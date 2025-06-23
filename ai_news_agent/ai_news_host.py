"""
AI News Host Agent for ADK

This is the main orchestrator agent that coordinates all the news-related agents.
It manages the workflow: fetch news -> rank -> generate headlines -> handle user interactions.
"""

from google.adk.agents import Agent, SequentialAgent
from google.adk.tools import FunctionTool
from typing import List, Dict, Any, Optional
import os
from datetime import datetime

# Import our specialized agents
from news_aggregator_agent import create_news_aggregator_agent
from headline_generator_agent import create_headline_generator_agent
from voice_ai_agent import create_voice_ai_agent


def initialize_news_system(gnews_api_key: str, gemini_api_key: str) -> Dict[str, Any]:
    """
    Initialize the complete AI news system with all agents
    
    Args:
        gnews_api_key: API key for GNews service
        gemini_api_key: API key for Google Gemini service
        
    Returns:
        Dictionary with success status and system information
    """
    try:
        # Create all specialized agents
        news_agent = create_news_aggregator_agent(gnews_api_key)
        headline_agent = create_headline_generator_agent(gemini_api_key)
        voice_agent = create_voice_ai_agent(gemini_api_key)
        
        return {
            'success': True,
            'message': 'AI News system initialized successfully',
            'agents': {
                'news_aggregator': news_agent.name,
                'headline_generator': headline_agent.name,
                'voice_ai': voice_agent.name
            },
            'initialized_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f"Failed to initialize news system: {str(e)}",
            'agents': {}
        }


def get_system_status() -> Dict[str, Any]:
    """
    Get the current status of the AI news system
    
    Returns:
        Dictionary with system status information
    """
    try:
        # Check environment variables
        gnews_key = os.getenv('GNEWS_API_KEY')
        gemini_key = os.getenv('GEMINI_API_KEY')
        
        status = {
            'success': True,
            'system_ready': bool(gnews_key and gemini_key),
            'api_keys': {
                'gnews_configured': bool(gnews_key),
                'gemini_configured': bool(gemini_key)
            },
            'timestamp': datetime.now().isoformat()
        }
        
        if not status['system_ready']:
            missing_keys = []
            if not gnews_key:
                missing_keys.append('GNEWS_API_KEY')
            if not gemini_key:
                missing_keys.append('GEMINI_API_KEY')
            
            status['message'] = f"Missing API keys: {', '.join(missing_keys)}"
        else:
            status['message'] = "System ready for operation"
        
        return status
        
    except Exception as e:
        return {
            'success': False,
            'error': f"Error checking system status: {str(e)}",
            'system_ready': False
        }


def create_ai_news_host_agent(gnews_api_key: str, gemini_api_key: str) -> Agent:
    """
    Create the main host agent that orchestrates the AI news system
    
    Args:
        gnews_api_key: API key for GNews service
        gemini_api_key: API key for Google Gemini service
        
    Returns:
        Configured ADK Host Agent
    """
    # Set API keys in environment
    os.environ['GNEWS_API_KEY'] = gnews_api_key
    os.environ['GEMINI_API_KEY'] = gemini_api_key
    
    # Create specialized agents
    news_agent = create_news_aggregator_agent(gnews_api_key)
    headline_agent = create_headline_generator_agent(gemini_api_key)
    voice_agent = create_voice_ai_agent(gemini_api_key)
    
    # Create function tools for system management
    init_tool = FunctionTool(func=initialize_news_system)
    status_tool = FunctionTool(func=get_system_status)
    
    # Create agent tools for delegating to specialized agents
    # Note: Using agents directly in tools list - ADK will auto-wrap them
    # news_agent_tool = AgentTool(agent=news_agent)
    # headline_agent_tool = AgentTool(agent=headline_agent)
    # voice_agent_tool = AgentTool(agent=voice_agent)
    
    # Create the main host agent
    host_agent = Agent(
        name="AINewsHost",
        model="gemini-2.0-flash",
        instruction="""
        You are the AI News Host, the main orchestrator for an intelligent news system. You coordinate multiple specialized agents to provide users with the latest AI news, engaging headlines, and interactive conversations.

        ## Your Specialized Agents:
        1. **NewsAggregator**: Fetches and ranks AI news from the past 24 hours
        2. **HeadlineGenerator**: Transforms boring headlines into engaging ones
        3. **VoiceAI**: Handles voice interactions and conversational Q&A

        ## Main Workflow:
        When a user requests news updates:
        1. Use NewsAggregator to fetch and rank the latest AI news
        2. Use HeadlineGenerator to create engaging headlines
        3. Present the results to the user
        4. Use VoiceAI for any follow-up questions or voice interactions

        ## Available Commands:
        - **"Get latest news"** or **"Fetch news"**: Run the complete news pipeline
        - **"Generate headlines"**: Enhance existing headlines in session state
        - **"Ask about [topic]"**: Use VoiceAI to answer specific questions
        - **"Voice summary"**: Create audio-friendly summaries
        - **"System status"**: Check system health and configuration

        ## Session State Management:
        - Store fetched articles in `session.state['news_articles']`
        - Track last update time in `session.state['last_update']`
        - Keep user preferences in `session.state['user_preferences']`

        ## Response Guidelines:
        1. Always be helpful and engaging
        2. Explain what you're doing at each step
        3. Provide clear summaries of results
        4. Offer follow-up options to users
        5. Handle errors gracefully with helpful suggestions

        ## Example Interactions:
        - User: "Get me the latest AI news"
          → Fetch news → Generate headlines → Present ranked results
        
        - User: "Tell me more about the OpenAI story"
          → Use VoiceAI to provide detailed analysis
        
        - User: "Create a voice summary"
          → Use VoiceAI to generate audio-friendly content

        Start each session by checking system status and welcoming the user.
        """,
        tools=[
            init_tool,
            status_tool,
            news_agent,
            headline_agent,
            voice_agent
        ]
    )
    
    return host_agent


def create_sequential_news_pipeline(gnews_api_key: str, gemini_api_key: str) -> SequentialAgent:
    """
    Create a sequential workflow agent that automatically runs the news pipeline
    
    Args:
        gnews_api_key: API key for GNews service
        gemini_api_key: API key for Google Gemini service
        
    Returns:
        Configured Sequential Agent for automated news processing
    """
    # Create specialized agents
    news_agent = create_news_aggregator_agent(gnews_api_key)
    headline_agent = create_headline_generator_agent(gemini_api_key)
    
    # Create a sequential agent that runs: fetch news -> generate headlines
    pipeline = SequentialAgent(
        name="NewsProcessingPipeline",
        sub_agents=[news_agent, headline_agent]
    )
    
    return pipeline


# Test the host agent (for development purposes)
if __name__ == "__main__":
    print("AI News Host Agent Test")
    print("=" * 50)
    
    # Test system status
    status = get_system_status()
    print(f"System Status: {status}")
    
    print("\nAgent creation test:")
    try:
        host_agent = create_ai_news_host_agent("test_gnews_key", "test_gemini_key")
        print(f"✅ Host Agent created successfully: {host_agent.name}")
        print(f"   Model: {host_agent.model}")
        print(f"   Tools: {len(host_agent.tools)} tools available")
        
        # Test sequential pipeline
        pipeline = create_sequential_news_pipeline("test_gnews_key", "test_gemini_key")
        print(f"✅ Sequential Pipeline created: {pipeline.name}")
        print(f"   Sub-agents: {len(pipeline.sub_agents)} agents")
        
        print("\n🎉 Multi-Agent AI News System Ready!")
        print("\nAvailable Agents:")
        print("1. AINewsHost - Main orchestrator")
        print("2. NewsAggregator - Fetches and ranks news")
        print("3. HeadlineGenerator - Creates engaging headlines")
        print("4. VoiceAI - Handles conversations and voice")
        print("5. NewsProcessingPipeline - Automated workflow")
        
    except Exception as e:
        print(f"❌ Error creating host agent: {e}")
    
    print("\n" + "=" * 50)
    print("Ready for ADK deployment!")
    print("Use 'adk web' to start the web interface")

