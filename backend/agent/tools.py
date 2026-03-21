"""Concrete tool implementations for web research tasks."""
from typing import Any
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup

from agent.core.tools import Tool


class WebScraperTool(Tool):
    """Tool for scraping content from websites."""

    def __init__(self):
        super().__init__(
            name="scrape_website",
            description="Extract content from any URL",
        )

    def execute(self, url: str, max_chars: int = 2000) -> dict[str, Any]:
        """Scrape content from a URL.
        
        Args:
            url: Website URL to scrape.
            max_chars: Maximum characters to return.
            
        Returns:
            Dictionary with scraped content.
        """
        try:
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            for script in soup(["script", "style"]):
                script.decompose()

            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
            text = "".join(chunk for chunk in chunks if chunk)
            text = text[:max_chars]

            return {
                "url": url,
                "title": soup.title.string if soup.title else "No title",
                "content": text,
                "status": "success",
            }
        except Exception as e:
            return {"url": url, "error": str(e), "status": "failed"}


class GoogleSearchTool(Tool):
    """Tool for searching Google."""

    def __init__(self):
        super().__init__(
            name="google_search",
            description="Search Google and return top results",
        )

    def execute(self, query: str, num_results: int = 5) -> list[dict[str, str]]:
        """Search Google for query.
        
        Args:
            query: Search query.
            num_results: Number of results to return.
            
        Returns:
            List of search results.
        """
        try:
            url = f"https://www.google.com/search?q={quote_plus(query)}"
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                "Accept": (
                    "text/html,application/xhtml+xml,"
                    "application/xml;q=0.9,*/*;q=0.8"
                ),
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip,deflate",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            results = []
            search_results = soup.find_all("div", class_="g")
            if not search_results:
                search_results = soup.find_all("div", {"data-sokoban-container": True})
            if not search_results:
                search_results = soup.find_all("div", class_="tF2Cxc")

            for g in search_results[:num_results]:
                try:
                    title_elem = g.find("h3")
                    if not title_elem:
                        continue
                    title = title_elem.get_text()
                    link_elem = g.find("a")
                    if not link_elem or "href" not in link_elem.attrs:
                        continue
                    link = link_elem["href"]

                    snippet = ""
                    snippet_elem = g.find("div", class_="VwiC3b")
                    if not snippet_elem:
                        snippet_elem = g.find("span", class_="aCOpRe")
                    if not snippet_elem:
                        snippet_elem = g.find("div", class_="s")
                    if snippet_elem:
                        snippet = snippet_elem.get_text()

                    if title and link:
                        results.append({
                            "title": title,
                            "link": link,
                            "snippet": snippet or "No description available",
                        })
                except Exception:
                    continue

            if not results:
                return [{
                    "title": "Search limitation",
                    "snippet": (
                        f"Unable to fetch results for '{query}'. "
                        "Try using the direct 'wiki' command for encyclopedia info."
                    ),
                    "link": f"https://www.google.com/search?q={quote_plus(query)}",
                }]

            return results
        except Exception as e:
            return [{
                "error": str(e),
                "title": "Search failed",
                "snippet": f"Could not complete search for '{query}'.",
                "link": f"https://www.google.com/search?q={quote_plus(query)}",
            }]


class WikipediaTool(Tool):
    """Tool for fetching Wikipedia summaries."""

    def __init__(self):
        super().__init__(
            name="wikipedia",
            description="Get information from Wikipedia",
        )

    def execute(self, topic: str) -> dict[str, Any]:
        """Fetch Wikipedia summary.
        
        Args:
            topic: Wikipedia article topic.
            
        Returns:
            Dictionary with Wikipedia data.
        """
        try:
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote_plus(topic)}"
            headers = {"User-Agent": "ResearchAgent/1.0 (Educational Purpose)"}
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 404:
                return {
                    "error": f"Article not found for '{topic}'",
                    "status": "not_found",
                }

            response.raise_for_status()
            data = response.json()

            if "title" not in data:
                return {"error": "Article not found", "status": "invalid_response"}

            return {
                "title": data.get("title", "unknown"),
                "summary": data.get("extract", "No summary available"),
                "url": data.get("content_urls", {}).get("desktop", {}).get("page", ""),
                "status": "success",
            }
        except requests.exceptions.RequestException as e:
            return {"error": f"Network error: {e}", "status": "network_error"}
        except Exception as e:
            return {"error": str(e), "status": "error"}


class NewsTool(Tool):
    """Tool for fetching news headlines."""

    def __init__(self):
        super().__init__(
            name="get_news",
            description="Get latest news headlines",
        )

    def execute(self, topic: str = "technology") -> list[dict[str, str]]:
        """Fetch news for topic.
        
        Args:
            topic: News topic.
            
        Returns:
            List of news articles.
        """
        try:
            url = f"https://www.google.com/search?q={quote_plus(topic)}"
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/91.0.4472.124 Safari/537.36"
                )
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            articles = []
            for article in soup.find_all("article")[:10]:
                try:
                    title_element = article.find("a")
                    if title_element and title_element.get_text(strip=True):
                        href = title_element.get("href", "")
                        if href.startswith("./"):
                            href = "https://news.google.com" + href[1:]
                        elif not href.startswith("http"):
                            href = "https://news.google.com" + href
                        articles.append({
                            "title": title_element.get_text(strip=True),
                            "link": href,
                        })
                except Exception:
                    continue

            if not articles:
                return [{
                    "title": f"News search for '{topic}'",
                    "link": url,
                    "note": "Unable to fetch news automatically.",
                }]

            return articles[:10]
        except Exception as e:
            return [{
                "error": str(e),
                "title": f"Could not fetch news for '{topic}'",
                "link": f"https://news.google.com/search?q={quote_plus(topic)}",
            }]


class WeatherTool(Tool):
    """Tool for fetching weather data."""

    def __init__(self):
        super().__init__(
            name="get_weather",
            description="Get current weather for any city",
        )

    def execute(self, city: str) -> dict[str, Any]:
        """Fetch weather for city.
        
        Args:
            city: City name.
            
        Returns:
            Dictionary with weather data.
        """
        try:
            url = f"https://wttr.in/{quote_plus(city)}?format=j1"
            response = requests.get(url, timeout=10)
            data = response.json()
            current = data["current_condition"][0]

            return {
                "city": city,
                "temperature_c": current["temp_C"],
                "temperature_f": current["temp_F"],
                "condition": current["weatherDesc"][0]["value"],
                "humidity": current["humidity"],
                "wind_speed_kph": current["windspeedKmph"],
                "feels_like_c": current["FeelsLikeC"],
                "feels_like_f": current["FeelsLikeF"],
                "status": "success",
            }
        except Exception as e:
            return {"error": str(e), "city": city, "status": "error"}
