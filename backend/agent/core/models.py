"""Pydantic models for data validation."""
from pydantic import BaseModel, Field
from typing import Optional, Any


class WeatherResponse(BaseModel):
    """Response model for weather data."""
    city: str
    temperature_c: str
    temperature_f: str
    condition: str
    humidity: str
    wind_speed_kph: str
    feels_like_c: str
    feels_like_f: str
    status: str = "success"


class WikipediaResponse(BaseModel):
    """Response model for Wikipedia data."""
    title: str
    summary: str
    url: str
    status: str = "success"
    error: Optional[str] = None


class SearchResult(BaseModel):
    """Single search result item."""
    title: str
    link: str
    snippet: str


class SearchResponse(BaseModel):
    """Response model for search results."""
    results: list[SearchResult]
    status: str = "success"
    error: Optional[str] = None


class ScrapeResponse(BaseModel):
    """Response model for scraped content."""
    url: str
    title: str
    content: str
    status: str = "success"
    error: Optional[str] = None


class NewsArticle(BaseModel):
    """Single news article item."""
    title: str
    link: str


class NewsResponse(BaseModel):
    """Response model for news data."""
    articles: list[NewsArticle]
    status: str = "success"
    error: Optional[str] = None


class AgentRequest(BaseModel):
    """Request model for agent interaction."""
    message: str
    use_memory: bool = True
    session_id: Optional[str] = None


class AgentResponse(BaseModel):
    """Response model for agent interaction."""
    response: str
    tool_used: Optional[str] = None
    tool_result: Optional[Any] = None
    status: str = "success"
    error: Optional[str] = None
