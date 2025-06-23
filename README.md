# AI News Agent - ADK Multi-Agent System

A sophisticated multi-agent AI news system built with Google's Agent Development Kit (ADK) that provides users with ranked AI news, engaging headlines, and interactive voice conversations.

## 🎯 Features

### 📰 **Intelligent News Aggregation**
- Fetches top 10 AI news from the past 24 hours
- Uses GNews API for reliable, real-time sources
- Smart ranking algorithm (least → most interesting)
- Interest levels: 📰 NEWS → 📈 TRENDING → ⚡ HOT → 🔥 BREAKING

### ✨ **AI-Powered Headlines**
- Transforms boring headlines into engaging, clickable ones
- Uses Google Gemini API for creative writing
- Maintains factual accuracy while adding excitement
- Automatic excitement level assignment

### 🎤 **Voice AI Integration**
- Natural voice interactions and conversations
- Speech-to-text and text-to-speech capabilities
- Interactive Q&A about any news article
- Audio-friendly news summaries

### 🤖 **Multi-Agent Architecture**
Built using ADK's multi-agent patterns:
- **NewsAggregator**: Fetches and ranks news articles
- **HeadlineGenerator**: Creates engaging headlines
- **VoiceAI**: Handles conversational interactions
- **AINewsHost**: Main orchestrator agent

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  NewsAggregator │    │HeadlineGenerator│    │    VoiceAI      │
│     Agent       │    │     Agent       │    │     Agent       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │  AINewsHost     │
                    │     Agent       │
                    │ (Orchestrator)  │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │   ADK Web UI    │
                    │  (Built-in UI)  │
                    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Google ADK installed
- API keys (both free):
  - GNews API key from [gnews.io](https://gnews.io/)
  - Google Gemini API key from [ai.google.dev](https://ai.google.dev/)

### Installation

1. **Clone/Download the project**
   ```bash
   # Extract the provided files to your desired directory
   cd adk_ai_news_agent
   ```

2. **Install dependencies**
   ```bash
   pip install google-adk google-generativeai requests
   ```

3. **Set up environment variables**
   ```bash
   export GNEWS_API_KEY="your_gnews_api_key_here"
   export GEMINI_API_KEY="your_gemini_api_key_here"
   ```

4. **Run with ADK**
   ```bash
   # Start web interface
   adk web

   # Or run in terminal
   adk run
   ```

5. **Access the application**
   - Web UI: Open the URL provided by `adk web` (typically http://localhost:8080)
   - Terminal: Interact directly in the command line

## 📁 Project Structure

```
adk_ai_news_agent/
├── agent.py                    # Main ADK entry point
├── news_aggregator_agent.py    # News fetching and ranking
├── headline_generator_agent.py # Headline enhancement
├── voice_ai_agent.py          # Voice interactions
├── ai_news_host.py            # Host agent (orchestrator)
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## 🎮 Usage Guide

### Basic Commands

Once the system is running, you can interact with it using natural language:

**Get Latest News:**
```
"Get me the latest AI news"
"Fetch today's AI developments"
"What's happening in AI today?"
```

**Generate Engaging Headlines:**
```
"Make the headlines more exciting"
"Generate engaging headlines"
"Refresh the headlines"
```

**Ask Specific Questions:**
```
"Tell me more about the OpenAI story"
"What's the most important news today?"
"Explain the breakthrough in simple terms"
```

**Voice Interactions:**
```
"Create a voice summary"
"Give me an audio briefing"
"I want to ask a voice question"
```

### Example Interaction Flow

1. **Start**: "Get latest AI news"
   → System fetches and ranks 10 articles

2. **Enhance**: "Generate engaging headlines"
   → Headlines become more clickable and exciting

3. **Explore**: "Tell me about the most interesting story"
   → Detailed analysis of the top-ranked article

4. **Listen**: "Create a brief audio summary"
   → Audio-friendly summary for listening

## 🔧 Configuration

### API Keys Setup

**GNews API (Free Tier: 100 requests/day)**
1. Visit [gnews.io](https://gnews.io/)
2. Sign up for free account
3. Get API key from dashboard
4. Set `GNEWS_API_KEY` environment variable

**Google Gemini API (Free Tier Available)**
1. Visit [ai.google.dev](https://ai.google.dev/)
2. Create Google Cloud project
3. Enable Gemini API
4. Generate API key
5. Set `GEMINI_API_KEY` environment variable

### Environment Variables

Create a `.env` file or set environment variables:

```bash
# Required API Keys
GNEWS_API_KEY=your_gnews_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Optional Configuration
NEWS_MAX_ARTICLES=10
NEWS_HOURS_BACK=24
```

## 🎯 Agent Capabilities

### NewsAggregator Agent
- **Function**: Fetches AI news from GNews API
- **Ranking**: Intelligent interest scoring (1-10)
- **Keywords**: Tracks breakthrough, revolutionary, major announcements
- **Output**: Ranked articles stored in session state

### HeadlineGenerator Agent  
- **Function**: Enhances headlines using Gemini AI
- **Styles**: Adapts excitement level to interest score
- **Accuracy**: Maintains factual integrity
- **Output**: Engaging, clickable headlines

### VoiceAI Agent
- **Function**: Handles conversational interactions
- **Capabilities**: Q&A, summaries, voice processing
- **Modes**: Brief, detailed, or highlights summaries
- **Output**: Natural, voice-friendly responses

### AINewsHost Agent
- **Function**: Main orchestrator and user interface
- **Coordination**: Manages workflow between agents
- **Session**: Maintains state and user preferences
- **Interface**: Primary interaction point for users

## 🔄 Workflow

1. **News Fetching**: NewsAggregator gets latest articles
2. **Ranking**: Articles sorted by interest level (1-10)
3. **Enhancement**: HeadlineGenerator creates engaging titles
4. **Interaction**: VoiceAI handles user questions and summaries
5. **Orchestration**: AINewsHost coordinates everything

## 🌐 ADK Integration

This system leverages ADK's powerful features:

- **Multi-Agent Coordination**: Specialized agents work together
- **Built-in UI**: Uses ADK's web interface (no custom UI needed)
- **Session Management**: Automatic state handling
- **Tool Integration**: Seamless function calling
- **Voice Support**: Built-in speech capabilities

## 🆓 Free Tier Limits

**GNews API:**
- 100 requests per day
- 10 articles per request
- Real-time news access

**Google Gemini API:**
- Generous free tier
- Rate limits apply
- Suitable for development and testing

## 🚀 Deployment Options

### Local Development
```bash
adk web  # Start local web server
```

### Production Deployment
- Deploy to Google Cloud Run
- Use ADK's deployment features
- Configure environment variables
- Set up monitoring and logging

## 🛠️ Troubleshooting

### Common Issues

**"Module not found" errors:**
```bash
pip install google-adk google-generativeai requests
```

**API key errors:**
```bash
# Check environment variables
echo $GNEWS_API_KEY
echo $GEMINI_API_KEY
```

**No news articles found:**
- Check GNews API key validity
- Verify internet connection
- Check API rate limits

**Headline generation fails:**
- Verify Gemini API key
- Check API quotas
- Ensure proper model access

### Debug Mode

Run with debug information:
```bash
export ADK_DEBUG=true
adk run
```

## 📈 Performance

- **Response Time**: ~2-5 seconds for complete workflow
- **Accuracy**: High-quality news ranking and headlines
- **Reliability**: Graceful error handling and fallbacks
- **Scalability**: Designed for production use

## 🔮 Future Enhancements

- **Multiple News Sources**: Integrate additional APIs
- **Personalization**: User preference learning
- **Real-time Updates**: WebSocket-based live updates
- **Advanced Analytics**: Trend analysis and insights
- **Mobile App**: Native mobile interface

## 📄 License

MIT License - Feel free to use and modify for your projects.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make improvements
4. Test thoroughly
5. Submit pull request

