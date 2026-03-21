"""Configuration management for the agent system."""
from dataclasses import dataclass
from typing import Optional
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass
class AgentConfig:
    """Configuration for the AI agent."""
    model: str = "gpt-4o"
    max_history: int = 100
    max_retries: int = 3
    temperature: float = 0.7
    require_approval: bool = False
    auto_approve_threshold: float = 0.0


@dataclass
class APIConfig:
    """Configuration for API settings."""
    openai_api_key: Optional[str] = None
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: list[str] = None

    def __post_init__(self):
        if self.openai_api_key is None:
            self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.cors_origins is None:
            self.cors_origins = ["http://localhost:5173", "http://localhost:3000"]


@dataclass
class ToolConfig:
    """Configuration for tools."""
    search_limit: int = 5
    scrape_max_chars: int = 2000
    request_timeout: int = 10
