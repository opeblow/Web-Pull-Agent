"""FastAPI application entry point."""
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from agent.core.agent import Agent
from agent.tools import (
    WebScraperTool,
    GoogleSearchTool,
    WikipediaTool,
    NewsTool,
    WeatherTool,
)


AGENT_SYSTEM_PROMPT = """You are a research assistant that helps users find information.

Your capabilities:
- scrape_website: Extract content from any URL
- google_search: Search Google for information
- wikipedia: Get Wikipedia articles
- get_news: Get latest news headlines
- get_weather: Get current weather for any city

When you need to use a tool, respond EXACTLY like this:
USE_TOOL:tool_name
PARAMS:param1=value1,param2=value2

Examples:
User asks: "What's the weather in London?"
USE_TOOL:get_weather
PARAMS:city=London

User asks: "Tell me about Bitcoin"
USE_TOOL:wikipedia
PARAMS:topic=Bitcoin

After the tool returns data, I will ask you to explain the results."""


session_agents: dict[str, Agent] = {}


def get_agent(session_id: str, api_key: str) -> Agent:
    """Get or create agent for session."""
    if session_id not in session_agents:
        agent = Agent(
            name="RESEARCH_AGENT",
            system_prompt=AGENT_SYSTEM_PROMPT,
            api_key=api_key,
            model="gpt-4o",
            require_approval=False,
            max_retries=3,
            max_history=100,
        )
        agent.register_tool(WebScraperTool())
        agent.register_tool(GoogleSearchTool())
        agent.register_tool(WikipediaTool())
        agent.register_tool(NewsTool())
        agent.register_tool(WeatherTool())
        session_agents[session_id] = agent
    return session_agents[session_id]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler."""
    yield
    session_agents.clear()


app = FastAPI(
    title="WebPull Agent API",
    description="AI-powered research assistant for web scraping, search, and more",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    """Chat request model."""
    message: str
    session_id: str = "default"
    use_memory: bool = True


class ToolRequest(BaseModel):
    """Direct tool execution request."""
    tool_name: str
    session_id: str = "default"
    params: dict[str, Any] = {}


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    tool_used: str | None = None
    tool_result: Any = None
    status: str = "success"


class ToolResponse(BaseModel):
    """Tool execution response."""
    result: Any
    status: str = "success"


class StatusResponse(BaseModel):
    """Agent status response."""
    status: dict[str, Any]
    tools: list[str]


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(status="healthy", version="1.0.0")


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Chat with the agent."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY not configured",
        )

    try:
        agent = get_agent(request.session_id, api_key)
        response = agent.run(request.message, use_memory=request.use_memory)

        tool_used = None
        tool_result = None
        if "USE_TOOL:" in response:
            tool_used = "auto_detected"

        return ChatResponse(
            response=response,
            tool_used=tool_used,
            tool_result=tool_result,
        )
    except Exception as e:
        return ChatResponse(
            response=f"Error: {str(e)}",
            status="error",
        )


@app.post("/tool", response_model=ToolResponse)
async def execute_tool(request: ToolRequest) -> ToolResponse:
    """Execute a specific tool directly."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY not configured",
        )

    try:
        agent = get_agent(request.session_id, api_key)
        result = agent.execute_tool(request.tool_name, **request.params)

        if result.get("success"):
            return ToolResponse(result=result.get("result"))
        else:
            raise HTTPException(status_code=400, detail=result.get("error"))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status/{session_id}", response_model=StatusResponse)
async def get_status(session_id: str) -> StatusResponse:
    """Get agent status for a session."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY not configured",
        )

    if session_id not in session_agents:
        raise HTTPException(status_code=404, detail="Session not found")

    agent = session_agents[session_id]
    return StatusResponse(
        status=agent.get_status(),
        tools=agent.tools.list_tools(),
    )


@app.delete("/session/{session_id}")
async def delete_session(session_id: str) -> JSONResponse:
    """Delete a session and clear its memory."""
    if session_id in session_agents:
        del session_agents[session_id]
    return JSONResponse({"status": "deleted", "session_id": session_id})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
