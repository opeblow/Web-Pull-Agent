# WebPull Agent

<p align="center">
  <img src="frontend/public/favicon.svg" alt="WebPull Agent Logo" width="120" />
</p>

<p align="center">
  <strong>AI-Powered Research Assistant</strong>
</p>

<p align="center">
  A modular AI agent framework for web research, search, and data extraction — built with FastAPI + React.
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#api-reference">API</a> •
  <a href="#development">Development</a>
</p>

---

## Features

- **AI-Powered Intelligence**: Powered by GPT-4o for intelligent decision-making
- **Modular Tool System**: Extensible architecture with reusable tools
- **Web Scraping**: Extract content from any public URL
- **Google Search**: Search and retrieve top results
- **Wikipedia Integration**: Fetch instant article summaries
- **News Headlines**: Get latest news on any topic
- **Weather Data**: Real-time weather for any city
- **Modern UI**: Google-inspired dark theme interface
- **Session Management**: Persistent conversation memory

## Architecture

```
ope/
├── backend/                    # FastAPI Backend
│   ├── main.py                 # API entry point
│   ├── agent/                  # Agent framework
│   │   ├── core/              # Core building blocks
│   │   │   ├── agent.py       # Main Agent class
│   │   │   ├── intelligence.py # AI reasoning
│   │   │   ├── memory.py      # Conversation memory
│   │   │   ├── tools.py       # Tool base classes
│   │   │   ├── validation.py  # Data validation
│   │   │   ├── recovery.py    # Error handling
│   │   │   └── feedback.py    # Approval workflows
│   │   └── tools.py           # Tool implementations
│   ├── requirements.txt        # Python dependencies
│   └── .env.example           # Environment template
│
└── frontend/                   # React Frontend
    ├── src/
    │   ├── components/         # React components
    │   ├── context/           # React context providers
    │   ├── services/          # API client
    │   └── App.jsx           # Main application
    ├── package.json           # Node dependencies
    └── vite.config.js         # Vite configuration
```

---

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- OpenAI API key
- BRAVE API KEY

### 1. Clone & Setup Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 2. Setup Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

### 3. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
# Set your API key
export OPENAI_API_KEY=sk-your-key-here
       BRAVE_API_KEY=.....  # Linux/Mac
# set OPENAI_API_KEY=sk-your-key-here   # Windows (Command Prompt)

# Run the API server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Open your browser:**
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/docs

---

## Run Commands

### Backend Commands

| Command | Description |
|---------|-------------|
| `uvicorn main:app --reload` | Run API with hot reload |
| `uvicorn main:app --host 0.0.0.0 --port 8000` | Run API on specific port |
| `python -m uvicorn main:app --reload` | Alternative runner |

### Frontend Commands

| Command | Description |
|---------|-------------|
| `npm run dev` | Start dev server (port 5173) |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint |

---

## API Reference

### Endpoints

#### `POST /api/chat`
Chat with the AI agent.

```json
{
  "message": "What's the weather in London?",
  "session_id": "user_123",
  "use_memory": true
}
```

**Response:**
```json
{
  "response": "The weather in London is currently...",
  "tool_used": "get_weather",
  "status": "success"
}
```

#### `POST /api/tool`
Execute a specific tool directly.

```json
{
  "tool_name": "get_weather",
  "params": { "city": "Tokyo" },
  "session_id": "default"
}
```

#### `GET /api/status/{session_id}`
Get agent status and statistics.

#### `DELETE /api/session/{session_id}`
Clear session memory.

#### `GET /api/health`
Health check endpoint.

---

## Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `scrape_website` | Extract content from URL | `url`, `max_chars` |
| `google_search` | Search Google | `query`, `num_results` |
| `wikipedia` | Get Wikipedia summary | `topic` |
| `get_news` | Fetch news headlines | `topic` |
| `get_weather` | Get current weather | `city` |

---

## Development

### Project Structure

The codebase follows Google Python Style Guide for the backend and React best practices for the frontend.

### Backend Dependencies

```
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
pydantic>=2.5.3
openai>=1.12.0
requests>=2.31.0
beautifulsoup4>=4.12.3
python-dotenv>=1.0.1
```

### Frontend Dependencies

```
react@^18.2.0
react-dom@^18.2.0
react-router-dom@^6.21.0
lucide-react@^0.303.0
clsx@^2.1.0
```

---

## Environment Variables

Create a `.env` file in the `backend/` directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Get your API key from: https://platform.openai.com/api-keys

---

## Troubleshooting

### Common Issues

**`OPENAI_API_KEY not configured`**
- Make sure you've created the `.env` file with your API key
- Restart the backend server after adding the key

**CORS Errors**
- Ensure the backend is running on port 8000
- Check that frontend is running on port 5173

**Module not found errors**
- Run `pip install -r requirements.txt` in the backend
- Run `npm install` in the frontend

---

## License

MIT License - feel free to use and modify for your projects.

---

<p align="center">
  Built with love using FastAPI + React
</p>
