import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from models import Country
from app import db

logger = logging.getLogger(__name__)

class CountryDataProcessor:
    """Process and clean country data from the REST Countries API."""
    
    @staticmethod
    def process_country_data(country_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract and clean key fields from a country data dictionary.
        
        Args:
            country_data: Raw country data from the API.
            
        Returns:
            Dictionary with cleaned country data.
        """
        try:
            # Extract basic information
            processed_data = {
                "name": country_data.get("name", {}).get("common", "Unknown"),
                "official_name": country_data.get("name", {}).get("official", "Unknown"),
                "country_code": country_data.get("cca3", ""),
                "capital": ", ".join(country_data.get("capital", ["Unknown"])) if isinstance(country_data.get("capital"), list) else "Unknown",
                "region": country_data.get("region", "Unknown"),
                "subregion": country_data.get("subregion", "Unknown"),
                "population": country_data.get("population", 0),
                "area": country_data.get("area", 0.0),
                "flag_emoji": country_data.get("flag", ""),
                "flag_url": country_data.get("flags", {}).get("svg", ""),
                "independent": country_data.get("independent", True),
                "un_member": country_data.get("unMember", True),
                "last_updated": datetime.utcnow()
            }
            
            # Process currencies
            currencies = country_data.get("currencies", {})
            currency_list = []
            for code, details in currencies.items():
                currency_name = details.get("name", "Unknown")
                currency_symbol = details.get("symbol", "")
                currency_list.append(f"{code} ({currency_name}, {currency_symbol})")
            processed_data["currencies"] = ", ".join(currency_list)
            
            # Process languages
            languages = country_data.get("languages", {})
            processed_data["languages"] = ", ".join(languages.values())
            
            return processed_data
        
        except Exception as e:
            logger.error(f"Error processing country data: {str(e)}")
            # Return basic data even if processing failed
            return {
                "name": country_data.get("name", {}).get("common", "Unknown"),
                "official_name": country_data.get("name", {}).get("official", "Unknown"),
                "capital": "Unknown",
                "region": "Unknown",
                "population": 0,
                "area": 0.0,
                "last_updated": datetime.utcnow()
            }
    
    @staticmethod
    def process_countries_list(countries_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process a list of country data dictionaries.
        
        Args:
            countries_data: List of raw country data from the API.
            
        Returns:
            List of dictionaries with cleaned country data.
        """
        processed_countries = []
        for country_data in countries_data:
            processed_country = CountryDataProcessor.process_country_data(country_data)
            processed_countries.append(processed_country)
        
        return processed_countries
    
    @staticmethod
    def save_country_to_db(country_data: Dict[str, Any]) -> Optional[Country]:
        """
        Save processed country data to the database.
        
        Args:
            country_data: Processed country data dictionary.
            
        Returns:
            Country object if successful, None otherwise.
        """
        try:
            # Check if country already exists in the database
            existing_country = Country.query.filter_by(name=country_data["name"]).first()
            
            if existing_country:
                # Update existing country
                for key, value in country_data.items():
                    setattr(existing_country, key, value)
                db.session.commit()
                logger.info(f"Updated country: {existing_country.name}")
                return existing_country
            else:
                # Create new country
                new_country = Country(**country_data)
                db.session.add(new_country)
                db.session.commit()
                logger.info(f"Added new country: {new_country.name}")
                return new_country
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error saving country to database: {str(e)}")
            return None
    
    @staticmethod
    def save_countries_to_db(countries_data: List[Dict[str, Any]]) -> int:
        """
        Save a list of processed country data to the database.
        
        Args:
            countries_data: List of processed country data dictionaries.
            
        Returns:
            Number of countries successfully saved.
        """
        success_count = 0
        for country_data in countries_data:
            if CountryDataProcessor.save_country_to_db(country_data):
                success_count += 1
        
        logger.info(f"Successfully saved {success_count} out of {len(countries_data)} countries")
        return success_count
