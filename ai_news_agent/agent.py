"""
Main entry point for the ADK AI News Agent system

This file serves as the main agent.py file that ADK expects.
It creates and configures the complete multi-agent news system.
"""

import os
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

# Import our specialized agents
from news_aggregator_agent import create_news_aggregator_agent
from headline_generator_agent import create_headline_generator_agent
from voice_ai_agent import create_voice_ai_agent


def main():
    """
    Main function to create and return the AI News Host Agent
    This is the entry point that ADK will use
    """
    # Get API keys from environment
    gnews_api_key = os.getenv('GNEWS_API_KEY', 'your_gnews_api_key_here')
    gemini_api_key = os.getenv('GEMINI_API_KEY', 'your_gemini_api_key_here')
    
    # Create specialized agents
    news_agent = create_news_aggregator_agent(gnews_api_key)
    headline_agent = create_headline_generator_agent(gemini_api_key)
    voice_agent = create_voice_ai_agent(gemini_api_key)
    
    # Create the main host agent using sub_agents instead of tools
    host_agent = Agent(
        name="AINewsHost",
        model="gemini-2.0-flash",
        instruction="""
        🤖 **Welcome to AI News Agent!**
        
        I'm your intelligent AI news companion, powered by a multi-agent system that brings you the latest AI developments with engaging headlines and interactive conversations.

        ## What I Can Do:
        
        **📰 Latest News**: I fetch the top 10 AI news from the past 24 hours from reliable sources and rank them from least to most interesting.
        
        **✨ Engaging Headlines**: I transform boring headlines into exciting, clickable ones while maintaining factual accuracy.
        
        **🎤 Voice Interactions**: I can handle voice questions and provide conversational responses about any news story.
        
        **🔍 Deep Analysis**: Ask me specific questions about any article and I'll provide detailed insights and context.

        ## How to Use Me:
        
        1. **"Get latest news"** - I'll fetch and rank today's top AI stories
        2. **"Generate headlines"** - I'll make the headlines more engaging
        3. **"Tell me about [topic]"** - Ask specific questions about any story
        4. **"Create voice summary"** - Get an audio-friendly news briefing
        
        ## My Multi-Agent Team:
        I coordinate with specialized agents to provide comprehensive news services. When you ask for news, I'll work with my team to fetch, rank, enhance, and present the information in the most engaging way possible.
        
        Ready to explore today's AI developments? Just ask me to "get latest news" to start!
        """,
        sub_agents=[news_agent, headline_agent, voice_agent]
    )
    
    return host_agent


# For ADK compatibility - expose as root_agent
root_agent = main()

if __name__ == "__main__":
    print("🤖 AI News Agent System")
    print("=" * 50)
    print("✅ Multi-agent system initialized successfully!")
    print(f"   Main Agent: {agent.name}")
    print(f"   Model: {agent.model}")
    print(f"   Specialized Agents: {len(agent.tools)} available")
    print("\n🚀 Ready for ADK deployment!")
    print("   Use 'adk web' to start the web interface")
    print("   Or 'adk run' to run in terminal mode")
    print("\n📋 Required Environment Variables:")
    print("   - GNEWS_API_KEY: Get from https://gnews.io/")
    print("   - GEMINI_API_KEY: Get from https://ai.google.dev/")
    print("\n" + "=" * 50)

