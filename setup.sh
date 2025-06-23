#!/bin/bash

# AI News Agent Setup Script
# This script helps set up the ADK AI News Agent system

echo "🤖 AI News Agent Setup"
echo "======================"

# Check if Python 3.11+ is available
if ! command -v python3.11 &> /dev/null; then
    echo "❌ Python 3.11+ is required but not found"
    echo "   Please install Python 3.11 or later"
    exit 1
fi

echo "✅ Python 3.11+ found"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not found"
    echo "   Please install pip3"
    exit 1
fi

echo "✅ pip3 found"

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Check if environment variables are set
echo "🔑 Checking API keys..."

if [ -z "$GNEWS_API_KEY" ]; then
    echo "⚠️  GNEWS_API_KEY not set"
    echo "   Get your free API key from: https://gnews.io/"
    echo "   Then run: export GNEWS_API_KEY=your_key_here"
    MISSING_KEYS=true
fi

if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  GEMINI_API_KEY not set"
    echo "   Get your free API key from: https://ai.google.dev/"
    echo "   Then run: export GEMINI_API_KEY=your_key_here"
    MISSING_KEYS=true
fi

if [ "$MISSING_KEYS" = true ]; then
    echo ""
    echo "📋 Setup Instructions:"
    echo "1. Get API keys from the URLs above"
    echo "2. Set environment variables:"
    echo "   export GNEWS_API_KEY=your_gnews_key"
    echo "   export GEMINI_API_KEY=your_gemini_key"
    echo "3. Run the system:"
    echo "   adk web    # For web interface"
    echo "   adk run    # For terminal interface"
else
    echo "✅ All API keys configured"
    echo ""
    echo "🚀 Ready to run!"
    echo "   adk web    # Start web interface"
    echo "   adk run    # Start terminal interface"
fi

echo ""
echo "📁 Project Structure:"
echo "   agent.py                    - Main ADK entry point"
echo "   news_aggregator_agent.py    - News fetching and ranking"
echo "   headline_generator_agent.py - Headline enhancement"
echo "   voice_ai_agent.py          - Voice interactions"
echo "   ai_news_host.py            - Host agent orchestrator"
echo ""
echo "🎯 Example Commands:"
echo "   'Get latest AI news'"
echo "   'Generate engaging headlines'"
echo "   'Tell me about the OpenAI story'"
echo "   'Create a voice summary'"
echo ""
echo "======================"
echo "Setup complete! 🎉"

