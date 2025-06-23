"""
News Aggregation and Ranking Agent for ADK

This agent fetches AI news from the past 24 hours and ranks them by interest level.
It uses the GNews API for news aggregation and implements a custom ranking algorithm.
"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from typing import List, Dict, Any, Optional
import requests
import json
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import os


@dataclass
class NewsArticle:
    title: str
    description: str
    url: str
    published_at: str
    source: str
    content: str = ""
    interest_score: int = 0
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return asdict(self)


def fetch_ai_news(hours_back: int = 24, max_articles: int = 10) -> Dict[str, Any]:
    """
    Fetch AI news from the past specified hours using GNews API
    
    Args:
        hours_back: Number of hours to look back for news (default: 24)
        max_articles: Maximum number of articles to fetch (default: 10)
        
    Returns:
        Dictionary with success status, articles list, and count
    """
    api_key = os.getenv('GNEWS_API_KEY')
    if not api_key:
        return {
            'success': False,
            'error': 'GNEWS_API_KEY environment variable not set',
            'articles': []
        }
    
    base_url = "https://gnews.io/api/v4"
    
    try:
        # Calculate the date range
        end_date = datetime.now()
        start_date = end_date - timedelta(hours=hours_back)
        
        # Format dates for API (ISO format)
        from_date = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        to_date = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Search parameters
        params = {
            'q': 'artificial intelligence OR AI OR machine learning OR deep learning OR neural networks OR LLM OR GPT OR generative AI',
            'lang': 'en',
            'country': 'us',
            'max': min(max_articles, 10),  # GNews free tier allows max 10 per request
            'from': from_date,
            'to': to_date,
            'sortby': 'publishedAt',
            'apikey': api_key
        }
        
        response = requests.get(f"{base_url}/search", params=params)
        response.raise_for_status()
        
        data = response.json()
        articles = []
        
        for article_data in data.get('articles', []):
            article = NewsArticle(
                title=article_data.get('title', ''),
                description=article_data.get('description', ''),
                url=article_data.get('url', ''),
                published_at=article_data.get('publishedAt', ''),
                source=article_data.get('source', {}).get('name', ''),
                content=article_data.get('content', '')
            )
            articles.append(article.to_dict())
        
        return {
            'success': True,
            'articles': articles,
            'count': len(articles)
        }
        
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': f"Error fetching news: {str(e)}",
            'articles': []
        }
    except json.JSONDecodeError as e:
        return {
            'success': False,
            'error': f"Error parsing response: {str(e)}",
            'articles': []
        }


def rank_news_articles(articles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Rank news articles from least to most interesting based on keywords and recency
    
    Args:
        articles: List of article dictionaries
        
    Returns:
        Dictionary with success status and ranked articles
    """
    try:
        # Keywords that indicate high interest/sensational AI news
        high_interest_keywords = [
            'breakthrough', 'revolutionary', 'game-changing', 'unprecedented',
            'major', 'significant', 'groundbreaking', 'milestone', 'record',
            'first ever', 'world first', 'historic', 'dramatic', 'shocking',
            'surprising', 'unexpected', 'controversial', 'debate', 'concern',
            'warning', 'threat', 'risk', 'danger', 'safety', 'regulation',
            'ban', 'lawsuit', 'investigation', 'scandal', 'leak',
            'OpenAI', 'Google', 'Microsoft', 'Meta', 'Apple', 'Tesla',
            'ChatGPT', 'GPT-5', 'Gemini', 'Claude', 'AGI', 'superintelligence'
        ]
        
        medium_interest_keywords = [
            'new', 'latest', 'update', 'release', 'launch', 'announce',
            'develop', 'improve', 'enhance', 'advance', 'progress',
            'research', 'study', 'report', 'analysis', 'trend',
            'market', 'industry', 'business', 'investment', 'funding'
        ]
        
        def calculate_interest_score(article: Dict[str, Any]) -> int:
            """Calculate interest score for an article (1-10, 10 being most interesting)"""
            score = 1  # Base score
            text = f"{article.get('title', '')} {article.get('description', '')}".lower()
            
            # High interest keywords (add 3 points each, max 6)
            high_matches = sum(1 for keyword in high_interest_keywords if keyword.lower() in text)
            score += min(high_matches * 3, 6)
            
            # Medium interest keywords (add 1 point each, max 2)
            medium_matches = sum(1 for keyword in medium_interest_keywords if keyword.lower() in text)
            score += min(medium_matches, 2)
            
            # Recency bonus (newer articles get slight boost)
            try:
                pub_date = datetime.fromisoformat(article.get('published_at', '').replace('Z', '+00:00'))
                hours_old = (datetime.now().replace(tzinfo=pub_date.tzinfo) - pub_date).total_seconds() / 3600
                if hours_old < 6:
                    score += 1
                elif hours_old < 12:
                    score += 0.5
            except:
                pass  # Skip if date parsing fails
            
            # Cap at 10
            return min(int(score), 10)
        
        # Calculate interest scores
        for article in articles:
            article['interest_score'] = calculate_interest_score(article)
        
        # Sort by interest score (ascending - least to most interesting)
        ranked_articles = sorted(articles, key=lambda x: x['interest_score'])
        
        return {
            'success': True,
            'ranked_articles': ranked_articles,
            'count': len(ranked_articles)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f"Error ranking articles: {str(e)}",
            'ranked_articles': articles  # Return original list on error
        }


def create_news_aggregator_agent(gnews_api_key: str) -> Agent:
    """
    Create an ADK Agent for news aggregation and ranking
    
    Args:
        gnews_api_key: API key for GNews service
        
    Returns:
        Configured ADK Agent
    """
    # Set the API key in environment for the functions to use
    os.environ['GNEWS_API_KEY'] = gnews_api_key
    
    # Create function tools
    fetch_tool = FunctionTool(func=fetch_ai_news)
    rank_tool = FunctionTool(func=rank_news_articles)
    
    # Create the agent with tools
    agent = Agent(
        name="NewsAggregator",
        model="gemini-2.0-flash",
        instruction="""
        You are a news aggregation agent specialized in AI news. Your job is to:
        
        1. Fetch the latest AI news from the past 24 hours using the fetch_ai_news function
        2. Rank the articles from least to most interesting using the rank_news_articles function
        3. Store the ranked articles in the session state for other agents to use
        4. Provide a summary of the fetched and ranked news
        
        When a user asks for news, follow this sequence:
        1. Call fetch_ai_news() to get the latest articles
        2. If successful, call rank_news_articles() with the fetched articles
        3. Store the results in session state under 'news_articles' key
        4. Provide a summary showing the top 3 most interesting headlines
        
        If any step fails, explain the error and suggest next steps.
        Always be helpful and informative in your responses.
        """,
        tools=[fetch_tool, rank_tool]
    )
    
    return agent


# Test the agent (for development purposes)
if __name__ == "__main__":
    # Test the ranking function with mock data
    mock_articles = [
        {
            'title': "OpenAI Announces Revolutionary GPT-5 with Unprecedented Capabilities",
            'description': "OpenAI has unveiled GPT-5, marking a groundbreaking milestone in AI development with shocking new abilities.",
            'url': "https://example.com/1",
            'published_at': "2025-06-20T06:00:00Z",
            'source': "TechCrunch"
        },
        {
            'title': "New AI Research Shows Improved Language Understanding",
            'description': "Latest study reveals advances in natural language processing capabilities.",
            'url': "https://example.com/2",
            'published_at': "2025-06-20T04:00:00Z",
            'source': "AI News"
        },
        {
            'title': "Google Updates Gemini AI Model with Enhanced Features",
            'description': "Google announces new update to Gemini with improved performance and new capabilities.",
            'url': "https://example.com/3",
            'published_at': "2025-06-20T02:00:00Z",
            'source': "Google Blog"
        }
    ]
    
    # Test ranking function
    result = rank_news_articles(mock_articles)
    
    print("Mock Test Results:")
    print(f"Success: {result['success']}")
    print("Ranked Articles (Least to Most Interesting):")
    for i, article in enumerate(result['ranked_articles'], 1):
        print(f"{i}. [{article['interest_score']}/10] {article['title']}")
    
    print("\nAgent creation test:")
    try:
        agent = create_news_aggregator_agent("test_key")
        print(f"✅ Agent created successfully: {agent.name}")
        print(f"   Model: {agent.model}")
        print(f"   Tools: {len(agent.tools)} tools available")
    except Exception as e:
        print(f"❌ Error creating agent: {e}")

