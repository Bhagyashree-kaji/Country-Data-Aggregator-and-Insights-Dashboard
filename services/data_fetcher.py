import requests
import logging
from typing import List, Dict, Any, Optional
import time

logger = logging.getLogger(__name__)

class RestCountriesAPI:
    """Service to fetch data from the REST Countries API."""
    
    BASE_URL = "https://restcountries.com/v3.1"
    
    @staticmethod
    def fetch_all_countries() -> Optional[List[Dict[str, Any]]]:
        """
        Fetch data for all countries from the REST Countries API.
        
        Returns:
            List of country data dictionaries or None if the request fails.
        """
        try:
            logger.info("Fetching all countries data from REST Countries API")
            response = requests.get(f"{RestCountriesAPI.BASE_URL}/all")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching countries data: {str(e)}")
            return None
    
    @staticmethod
    def fetch_country_by_name(name: str) -> Optional[List[Dict[str, Any]]]:
        """
        Fetch data for a specific country by name.
        
        Args:
            name: The name of the country to fetch.
            
        Returns:
            Country data dictionary or None if the request fails.
        """
        try:
            logger.info(f"Fetching data for country: {name}")
            response = requests.get(f"{RestCountriesAPI.BASE_URL}/name/{name}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching country data for {name}: {str(e)}")
            return None
    
    @staticmethod
    def fetch_countries_by_region(region: str) -> Optional[List[Dict[str, Any]]]:
        """
        Fetch data for countries in a specific region.
        
        Args:
            region: The region to fetch countries for.
            
        Returns:
            List of country data dictionaries or None if the request fails.
        """
        try:
            logger.info(f"Fetching countries in region: {region}")
            response = requests.get(f"{RestCountriesAPI.BASE_URL}/region/{region}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching countries in region {region}: {str(e)}")
            return None
    
    @staticmethod
    def retry_fetch(fetch_function, *args, max_retries=3, delay=1, **kwargs):
        """
        Retry a fetch function with exponential backoff.
        
        Args:
            fetch_function: The function to retry.
            max_retries: Maximum number of retries.
            delay: Initial delay between retries (seconds).
            *args, **kwargs: Arguments to pass to the fetch function.
            
        Returns:
            Result of the fetch function or None if all retries fail.
        """
        for attempt in range(max_retries):
            result = fetch_function(*args, **kwargs)
            if result is not None:
                return result
            
            wait_time = delay * (2 ** attempt)
            logger.warning(f"Retry {attempt + 1}/{max_retries} after {wait_time}s")
            time.sleep(wait_time)
        
        logger.error(f"All {max_retries} retries failed")
        return None
