"""
Base scraper class with common functionality for all web scrapers.
Includes rate limiting, retry logic, and error handling.
"""

import time
import logging
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod
import requests
from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class BaseScraper(ABC):
    """Base class for all web scrapers with common functionality."""
    
    def __init__(self, delay: float = 2.0, max_retries: int = 3):
        """
        Initialize the base scraper.
        
        Args:
            delay: Delay in seconds between requests (rate limiting)
            max_retries: Maximum number of retry attempts for failed requests
        """
        self.delay = delay
        self.max_retries = max_retries
        self.logger = logging.getLogger(self.__class__.__name__)
        self.session = self._create_session()
        self.ua = UserAgent()
        self.last_request_time = 0
        
    def _create_session(self) -> requests.Session:
        """Create a requests session with retry logic."""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def _get_headers(self) -> Dict[str, str]:
        """Generate headers with rotating user agent."""
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    def _rate_limit(self):
        """Implement rate limiting between requests."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()
    
    def fetch_page(self, url: str, params: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Fetch a web page with rate limiting and error handling.
        
        Args:
            url: URL to fetch
            params: Optional query parameters
            
        Returns:
            Page content as string, or None if request failed
        """
        self._rate_limit()
        
        try:
            self.logger.info(f"Fetching: {url}")
            response = self.session.get(
                url,
                headers=self._get_headers(),
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.text
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching {url}: {str(e)}")
            return None
    
    @abstractmethod
    def scrape(self, *args, **kwargs):
        """
        Main scraping method to be implemented by subclasses.
        
        This method should contain the specific scraping logic for each data source.
        """
        pass
    
    def close(self):
        """Close the session."""
        self.session.close()
        self.logger.info("Session closed")
