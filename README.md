# FinBot — Stock Market Sentiment Chatbot

A Bloomberg-terminal-style Flask web app that combines live stock data,
news sentiment analysis, and AI-powered chat (Claude) in one interface.

## Features
- 🔴 Live stock quotes via Alpha Vantage
- 📰 News sentiment scoring via Alpha Vantage NEWS_SENTIMENT
- 🤖 AI chat powered by Anthropic Claude (claude-sonnet)
- 📊 Multi-stock comparison
- 🎨 Dark terminal UI with real-time ticker strip

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Get free API keys
| Service | URL | Free tier |
|---------|-----|-----------|
| Alpha Vantage | https://www.alphavantage.co/support/#api-key | 25 calls/day |
| NewsAPI (optional) | https://newsapi.org/register | 100 calls/day |
| Anthropic | https://console.anthropic.com | Pay-per-use |

### 3. Set environment variables
```bash
# Linux / macOS
export ALPHA_VANTAGE_KEY="your_key_here"
export ANTHROPIC_API_KEY="your_key_here"
export NEWS_API_KEY="your_key_here"   # optional

# Windows PowerShell
$env:ALPHA_VANTAGE_KEY = "your_key_here"
$env:ANTHROPIC_API_KEY = "your_key_here"
```

### 4. Run
```bash
python app.py
```
Open http://localhost:5000

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| POST | /api/stock | Fetch quote + news + sentiment for one ticker |
| POST | /api/chat  | Chat with Claude using live market context |
| POST | /api/compare | Compare up to 4 tickers side-by-side |

### /api/stock — Request
```json
{ "symbol": "AAPL" }
```

### /api/chat — Request
```json
{
  "history": [{"role":"user","content":"What's the sentiment?"}],
  "symbol": "AAPL",
  "context": { /* data from /api/stock */ }
}
```

### /api/compare — Request
```json
{ "symbols": ["AAPL", "MSFT", "NVDA"] }
```

## Architecture

```
app.py
├── fetch_quote()       → Alpha Vantage GLOBAL_QUOTE
├── fetch_news()        → Alpha Vantage NEWS_SENTIMENT (+ NewsAPI fallback)
├── compute_sentiment() → weighted score from news + price momentum
├── build_context()     → aggregates all data for a ticker
└── claude_chat()       → Anthropic /v1/messages with market context
```

## Notes
- Alpha Vantage free tier: 25 API calls/day. Use `demo` key to test (limited data).
- News sentiment requires Alpha Vantage Premium for full coverage.
- The AI chat works best with ANTHROPIC_API_KEY set.
