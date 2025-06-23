"""
Headline Generation Agent for ADK

This agent transforms boring news headlines into engaging, clickable ones
while maintaining factual accuracy. It uses Google Gemini API for creative writing.
"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from typing import List, Dict, Any, Optional
import google.generativeai as genai
import os
import json


def generate_engaging_headlines(articles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Transform boring headlines into engaging, clickable ones using Google Gemini API
    
    Args:
        articles: List of article dictionaries with original headlines
        
    Returns:
        Dictionary with success status and articles with new engaging headlines
    """
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return {
            'success': False,
            'error': 'GEMINI_API_KEY environment variable not set',
            'articles': articles
        }
    
    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        enhanced_articles = []
        
        for article in articles:
            original_title = article.get('title', '')
            description = article.get('description', '')
            interest_score = article.get('interest_score', 1)
            
            # Create prompt based on interest level
            if interest_score >= 8:
                excitement_level = "🔥 BREAKING"
                style = "extremely sensational and urgent"
            elif interest_score >= 6:
                excitement_level = "⚡ HOT"
                style = "very exciting and attention-grabbing"
            elif interest_score >= 4:
                excitement_level = "📈 TRENDING"
                style = "interesting and engaging"
            else:
                excitement_level = "📰 NEWS"
                style = "clear and informative"
            
            prompt = f"""
            Transform this AI news headline into a {style} version while maintaining factual accuracy:
            
            Original: "{original_title}"
            Description: "{description}"
            Interest Level: {interest_score}/10 ({excitement_level})
            
            Requirements:
            1. Make it more engaging and clickable
            2. Keep it factually accurate - don't add false information
            3. Use power words and emotional triggers appropriate for the interest level
            4. Keep it under 100 characters if possible
            5. Add the excitement level emoji at the start: {excitement_level}
            
            Return only the new headline, nothing else.
            """
            
            try:
                response = model.generate_content(prompt)
                new_headline = response.text.strip()
                
                # Create enhanced article
                enhanced_article = article.copy()
                enhanced_article['original_title'] = original_title
                enhanced_article['title'] = new_headline
                enhanced_article['excitement_level'] = excitement_level
                
                enhanced_articles.append(enhanced_article)
                
            except Exception as e:
                # If headline generation fails, keep original
                article['original_title'] = original_title
                article['excitement_level'] = excitement_level
                enhanced_articles.append(article)
                print(f"Warning: Failed to generate headline for '{original_title}': {e}")
        
        return {
            'success': True,
            'articles': enhanced_articles,
            'count': len(enhanced_articles)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f"Error generating headlines: {str(e)}",
            'articles': articles
        }


def create_summary_with_voice(articles: List[Dict[str, Any]], user_question: str = "") -> Dict[str, Any]:
    """
    Create a conversational summary of the news articles, optionally answering a specific question
    
    Args:
        articles: List of article dictionaries
        user_question: Optional specific question about the news
        
    Returns:
        Dictionary with success status and conversational response
    """
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return {
            'success': False,
            'error': 'GEMINI_API_KEY environment variable not set',
            'response': 'Sorry, I cannot provide a summary without API access.'
        }
    
    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Prepare articles summary for the prompt
        articles_text = ""
        for i, article in enumerate(articles, 1):
            articles_text += f"""
            {i}. {article.get('excitement_level', '📰')} {article.get('title', '')}
               Source: {article.get('source', 'Unknown')}
               Description: {article.get('description', '')}
               Interest Score: {article.get('interest_score', 1)}/10
               URL: {article.get('url', '')}
            """
        
        if user_question:
            prompt = f"""
            You are an AI news assistant. Here are today's top AI news articles:
            {articles_text}
            
            The user asked: "{user_question}"
            
            Please provide a helpful, conversational response that:
            1. Directly answers their question if possible
            2. References specific articles when relevant
            3. Provides additional context or insights
            4. Maintains an engaging, friendly tone
            5. Suggests follow-up questions they might find interesting
            
            Keep your response concise but informative (2-3 paragraphs max).
            """
        else:
            prompt = f"""
            You are an AI news assistant. Here are today's top AI news articles ranked from least to most interesting:
            {articles_text}
            
            Please provide a conversational summary that:
            1. Highlights the most interesting developments (top 3)
            2. Explains why these stories matter
            3. Connects related stories if any
            4. Uses an engaging, friendly tone
            5. Ends with an invitation for questions
            
            Keep it conversational and engaging (2-3 paragraphs max).
            """
        
        response = model.generate_content(prompt)
        summary = response.text.strip()
        
        return {
            'success': True,
            'response': summary,
            'articles_count': len(articles)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f"Error creating summary: {str(e)}",
            'response': 'Sorry, I encountered an error while creating the summary.'
        }


def create_headline_generator_agent(gemini_api_key: str) -> Agent:
    """
    Create an ADK Agent for headline generation and conversational AI
    
    Args:
        gemini_api_key: API key for Google Gemini service
        
    Returns:
        Configured ADK Agent
    """
    # Set the API key in environment for the functions to use
    os.environ['GEMINI_API_KEY'] = gemini_api_key
    
    # Create function tools
    headline_tool = FunctionTool(func=generate_engaging_headlines)
    summary_tool = FunctionTool(func=create_summary_with_voice)
    
    # Create the agent with tools
    agent = Agent(
        name="HeadlineGenerator",
        model="gemini-2.0-flash",
        instruction="""
        You are a headline generation and conversational AI agent specialized in AI news. Your job is to:
        
        1. Transform boring news headlines into engaging, clickable ones using generate_engaging_headlines
        2. Create conversational summaries and answer questions using create_summary_with_voice
        3. Maintain factual accuracy while making content more engaging
        4. Provide helpful, friendly responses to user questions about AI news
        
        When asked to generate headlines:
        1. Use generate_engaging_headlines() with the articles from session state
        2. Store the enhanced articles back in session state
        3. Show a summary of the transformations
        
        When asked questions about the news:
        1. Use create_summary_with_voice() with the articles and user question
        2. Provide conversational, helpful responses
        3. Reference specific articles when relevant
        
        Always be engaging, helpful, and maintain accuracy. Use emojis appropriately to make responses more lively.
        """,
        tools=[headline_tool, summary_tool]
    )
    
    return agent


# Test the agent (for development purposes)
if __name__ == "__main__":
    # Test the headline generation function with mock data
    mock_articles = [
        {
            'title': "OpenAI Announces New GPT Model",
            'description': "OpenAI has unveiled a new version of their GPT model with improved capabilities.",
            'url': "https://example.com/1",
            'published_at': "2025-06-20T06:00:00Z",
            'source': "TechCrunch",
            'interest_score': 8
        },
        {
            'title': "AI Research Shows Progress in Language Understanding",
            'description': "New study reveals advances in natural language processing capabilities.",
            'url': "https://example.com/2",
            'published_at': "2025-06-20T04:00:00Z",
            'source': "AI News",
            'interest_score': 4
        },
        {
            'title': "Google Updates AI Model",
            'description': "Google announces update to their AI model with new features.",
            'url': "https://example.com/3",
            'published_at': "2025-06-20T02:00:00Z",
            'source': "Google Blog",
            'interest_score': 6
        }
    ]
    
    print("Mock Test Results:")
    print("Original Headlines:")
    for i, article in enumerate(mock_articles, 1):
        print(f"{i}. [{article['interest_score']}/10] {article['title']}")
    
    # Test headline generation (would need real API key)
    print("\nNote: Headline generation requires GEMINI_API_KEY environment variable")
    print("Example enhanced headlines would be:")
    print("1. [8/10] 🔥 BREAKING OpenAI Drops Game-Changing GPT Model That Could Revolutionize AI Forever")
    print("2. [4/10] 📈 TRENDING Scientists Make Surprising Breakthrough in AI Language Understanding")
    print("3. [6/10] ⚡ HOT Google's Shocking AI Update Leaves Tech World Buzzing")
    
    print("\nAgent creation test:")
    try:
        agent = create_headline_generator_agent("test_key")
        print(f"✅ Agent created successfully: {agent.name}")
        print(f"   Model: {agent.model}")
        print(f"   Tools: {len(agent.tools)} tools available")
    except Exception as e:
        print(f"❌ Error creating agent: {e}")

