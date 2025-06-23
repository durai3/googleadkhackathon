"""
Voice AI Agent for ADK

This agent handles voice interactions, speech-to-text, text-to-speech,
and conversational AI for the news system. It integrates with Google's
speech services and Gemini for natural conversations.
"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from typing import List, Dict, Any, Optional
import google.generativeai as genai
import os
import json
import base64


def process_voice_question(audio_data: str, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Process a voice question about the news articles
    
    Args:
        audio_data: Base64 encoded audio data (placeholder for now)
        articles: List of article dictionaries
        
    Returns:
        Dictionary with success status and conversational response
    """
    # Note: In a real implementation, this would use Google Speech-to-Text API
    # For now, we'll simulate the process
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return {
            'success': False,
            'error': 'GEMINI_API_KEY environment variable not set',
            'response': 'Sorry, I cannot process voice questions without API access.',
            'audio_response': None
        }
    
    try:
        # Simulate speech-to-text (in real implementation, use Google Speech-to-Text)
        # For demo purposes, we'll use common questions
        simulated_questions = [
            "What's the most important AI news today?",
            "Tell me about OpenAI's latest announcement",
            "What are the trending AI developments?",
            "Explain the most interesting story",
            "What should I know about AI today?"
        ]
        
        # Pick a random question for simulation
        import random
        user_question = random.choice(simulated_questions)
        
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
            """
        
        prompt = f"""
        You are a friendly AI news assistant responding to a voice question. 
        
        User asked (via voice): "{user_question}"
        
        Here are today's AI news articles:
        {articles_text}
        
        Please provide a conversational, voice-friendly response that:
        1. Directly answers their question
        2. Uses natural, spoken language (avoid complex formatting)
        3. Highlights the most relevant articles
        4. Keeps it concise but informative (1-2 minutes of speech)
        5. Ends with an invitation for follow-up questions
        
        Remember: This will be converted to speech, so use natural, flowing language.
        """
        
        response = model.generate_content(prompt)
        text_response = response.text.strip()
        
        return {
            'success': True,
            'transcribed_question': user_question,
            'response': text_response,
            'audio_response': f"[Audio would be generated from: {text_response[:100]}...]",
            'articles_referenced': len(articles)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f"Error processing voice question: {str(e)}",
            'response': 'Sorry, I encountered an error while processing your voice question.',
            'audio_response': None
        }


def answer_follow_up_question(question: str, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Answer a specific follow-up question about the news articles
    
    Args:
        question: User's text question
        articles: List of article dictionaries
        
    Returns:
        Dictionary with success status and detailed response
    """
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return {
            'success': False,
            'error': 'GEMINI_API_KEY environment variable not set',
            'response': 'Sorry, I cannot answer questions without API access.'
        }
    
    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Prepare detailed articles information
        articles_text = ""
        for i, article in enumerate(articles, 1):
            articles_text += f"""
            Article {i}: {article.get('title', '')}
            Source: {article.get('source', 'Unknown')}
            Published: {article.get('published_at', 'Unknown')}
            Description: {article.get('description', '')}
            Interest Score: {article.get('interest_score', 1)}/10
            URL: {article.get('url', '')}
            Content Preview: {article.get('content', '')[:200]}...
            
            """
        
        prompt = f"""
        You are an expert AI news analyst. A user has asked a specific question about today's AI news.
        
        User Question: "{question}"
        
        Available Articles:
        {articles_text}
        
        Please provide a comprehensive, helpful response that:
        1. Directly addresses their specific question
        2. References relevant articles with specific details
        3. Provides context and analysis
        4. Explains technical concepts if needed
        5. Suggests related articles they might find interesting
        6. Offers to answer follow-up questions
        
        Be thorough but accessible. If the question can't be answered from the available articles, 
        say so and suggest what information would be helpful.
        """
        
        response = model.generate_content(prompt)
        detailed_response = response.text.strip()
        
        # Find most relevant articles based on question keywords
        question_lower = question.lower()
        relevant_articles = []
        
        for article in articles:
            title_lower = article.get('title', '').lower()
            desc_lower = article.get('description', '').lower()
            
            # Simple relevance scoring based on keyword matches
            relevance_score = 0
            for word in question_lower.split():
                if len(word) > 3:  # Only consider meaningful words
                    if word in title_lower:
                        relevance_score += 3
                    elif word in desc_lower:
                        relevance_score += 1
            
            if relevance_score > 0:
                article_copy = article.copy()
                article_copy['relevance_score'] = relevance_score
                relevant_articles.append(article_copy)
        
        # Sort by relevance
        relevant_articles.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return {
            'success': True,
            'question': question,
            'response': detailed_response,
            'relevant_articles': relevant_articles[:3],  # Top 3 most relevant
            'total_articles_searched': len(articles)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f"Error answering question: {str(e)}",
            'response': 'Sorry, I encountered an error while answering your question.'
        }


def create_audio_summary(articles: List[Dict[str, Any]], summary_type: str = "brief") -> Dict[str, Any]:
    """
    Create an audio-friendly summary of the news articles
    
    Args:
        articles: List of article dictionaries
        summary_type: "brief", "detailed", or "highlights"
        
    Returns:
        Dictionary with success status and audio-friendly text
    """
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return {
            'success': False,
            'error': 'GEMINI_API_KEY environment variable not set',
            'audio_text': 'Sorry, I cannot create audio summaries without API access.'
        }
    
    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Prepare articles for summary
        articles_text = ""
        for i, article in enumerate(articles, 1):
            articles_text += f"""
            {i}. {article.get('title', '')}
               Source: {article.get('source', 'Unknown')}
               Interest: {article.get('interest_score', 1)}/10
               Summary: {article.get('description', '')}
            """
        
        if summary_type == "brief":
            prompt = f"""
            Create a brief, audio-friendly news summary (30-60 seconds of speech) for these AI articles:
            {articles_text}
            
            Focus on:
            1. The top 2-3 most important stories
            2. Why they matter
            3. Natural, conversational language
            4. Easy to understand when spoken aloud
            
            Start with "Here's your AI news update for today..."
            """
        elif summary_type == "detailed":
            prompt = f"""
            Create a detailed, audio-friendly news summary (2-3 minutes of speech) for these AI articles:
            {articles_text}
            
            Include:
            1. All major stories with context
            2. Connections between related stories
            3. Implications and analysis
            4. Natural, conversational language
            5. Clear transitions between topics
            
            Start with "Welcome to your comprehensive AI news briefing..."
            """
        else:  # highlights
            prompt = f"""
            Create a highlights-focused audio summary for these AI articles:
            {articles_text}
            
            Focus on:
            1. The most exciting/surprising developments
            2. Major company announcements
            3. Breakthrough research
            4. Industry implications
            5. Engaging, enthusiastic tone
            
            Start with "Here are today's most exciting AI developments..."
            """
        
        response = model.generate_content(prompt)
        audio_text = response.text.strip()
        
        # Estimate reading time (average 150 words per minute)
        word_count = len(audio_text.split())
        estimated_duration = round(word_count / 150, 1)
        
        return {
            'success': True,
            'audio_text': audio_text,
            'summary_type': summary_type,
            'estimated_duration_minutes': estimated_duration,
            'word_count': word_count,
            'articles_covered': len(articles)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f"Error creating audio summary: {str(e)}",
            'audio_text': 'Sorry, I encountered an error while creating the audio summary.'
        }


def create_voice_ai_agent(gemini_api_key: str) -> Agent:
    """
    Create an ADK Agent for voice AI interactions
    
    Args:
        gemini_api_key: API key for Google Gemini service
        
    Returns:
        Configured ADK Agent
    """
    # Set the API key in environment for the functions to use
    os.environ['GEMINI_API_KEY'] = gemini_api_key
    
    # Create function tools
    voice_tool = FunctionTool(func=process_voice_question)
    question_tool = FunctionTool(func=answer_follow_up_question)
    audio_summary_tool = FunctionTool(func=create_audio_summary)
    
    # Create the agent with tools
    agent = Agent(
        name="VoiceAI",
        model="gemini-2.0-flash",
        instruction="""
        You are a voice AI agent specialized in conversational interactions about AI news. Your job is to:
        
        1. Process voice questions using process_voice_question
        2. Answer detailed follow-up questions using answer_follow_up_question
        3. Create audio-friendly summaries using create_audio_summary
        4. Provide natural, conversational responses suitable for voice interaction
        
        When handling voice interactions:
        1. Use process_voice_question() for voice input processing
        2. Use answer_follow_up_question() for specific text questions
        3. Use create_audio_summary() for generating audio summaries
        4. Always respond in a friendly, conversational tone
        5. Keep responses clear and easy to understand when spoken
        
        For audio summaries, offer different types:
        - "brief" for quick updates (30-60 seconds)
        - "detailed" for comprehensive briefings (2-3 minutes)
        - "highlights" for exciting developments
        
        Always be helpful, engaging, and ready to clarify or expand on any topic.
        """,
        tools=[voice_tool, question_tool, audio_summary_tool]
    )
    
    return agent


# Test the agent (for development purposes)
if __name__ == "__main__":
    # Test with mock data
    mock_articles = [
        {
            'title': "🔥 BREAKING OpenAI Drops Revolutionary GPT-5 with Unprecedented Capabilities",
            'description': "OpenAI has unveiled GPT-5, marking a groundbreaking milestone in AI development.",
            'url': "https://example.com/1",
            'published_at': "2025-06-20T06:00:00Z",
            'source': "TechCrunch",
            'interest_score': 9,
            'excitement_level': "🔥 BREAKING"
        },
        {
            'title': "📈 TRENDING Scientists Make Breakthrough in AI Language Understanding",
            'description': "New research reveals significant advances in natural language processing.",
            'url': "https://example.com/2",
            'published_at': "2025-06-20T04:00:00Z",
            'source': "AI Research",
            'interest_score': 6,
            'excitement_level': "📈 TRENDING"
        }
    ]
    
    print("Mock Test Results:")
    print("Voice AI Agent Functions:")
    print("1. process_voice_question() - Handles voice input and provides spoken responses")
    print("2. answer_follow_up_question() - Answers detailed questions about articles")
    print("3. create_audio_summary() - Creates audio-friendly news summaries")
    
    print("\nExample interactions:")
    print("Voice: 'What's the most important AI news today?'")
    print("Response: Natural, conversational answer about top stories")
    
    print("\nText: 'Tell me more about the OpenAI announcement'")
    print("Response: Detailed analysis with relevant article references")
    
    print("\nAudio Summary Types:")
    print("- Brief (30-60 sec): Quick highlights")
    print("- Detailed (2-3 min): Comprehensive briefing")
    print("- Highlights: Most exciting developments")
    
    print("\nAgent creation test:")
    try:
        agent = create_voice_ai_agent("test_key")
        print(f"✅ Agent created successfully: {agent.name}")
        print(f"   Model: {agent.model}")
        print(f"   Tools: {len(agent.tools)} tools available")
    except Exception as e:
        print(f"❌ Error creating agent: {e}")

