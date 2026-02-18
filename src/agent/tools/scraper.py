"""
Web scrapping and setiment extraction module.
This module integrate with firecrawl api to act as the eyes of the system. 
it searches for qualitative data news, analyst opinions and market rumours.
"""

from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from firecrawl import FirecrawlApp
from src.shared.config import settings

# Input Schema
class FirecrawlSearchInput(BaseModel):
    query : str = Field(..., description = "The search query string (e.g, 'NVDA recent analyst ratings')")

# Tool Defination
class SentimentalSearchTool(BaseTool):
    """
    Performs the semantic web search and returns the scraped content.
    Use firecrawl, extract full page content in markdown format.
    """
    name : str = "Search Stock News"
    
    description : str = ("Searches the web for the latest news, looks for analyst ratings, "
    "and surroundings market sentiment for a specific stock. Returns a summary for top 2 relevant artical and only extract top 50 words of it.")

    args_schema : Type[BaseModel] = FirecrawlSearchInput

    def _run(self, query: str) -> str:

        if not settings.firecrawl_api_key:
            return "Error: FireCrawl API key is missing in config"

        try:
            app = FirecrawlApp(api_key=settings.firecrawl_api_key)

            # Fetch top 2 articles
            result = app.search(
                query=query,
                limit=1,
                scrape_options={"formats": ["markdown"]}
            )

            return str(result)

        except Exception as e:
            return f"Error executing Firecrawl search: {str(e)}"

