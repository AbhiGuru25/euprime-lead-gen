"""
Location parser to identify biotech hubs and distinguish between
person location and company HQ location.
"""

from typing import Dict, Optional, Tuple
import re


class LocationParser:
    """Parse and analyze location data for lead scoring."""
    
    # Major biotech hubs with variations
    BIOTECH_HUBS = {
        'Boston/Cambridge': [
            'boston', 'cambridge, ma', 'cambridge ma', 'somerville', 
            'brookline', 'greater boston'
        ],
        'San Francisco Bay Area': [
            'san francisco', 'south san francisco', 'bay area', 
            'san mateo', 'palo alto', 'menlo park', 'redwood city',
            'oakland', 'berkeley', 'emeryville'
        ],
        'San Diego': ['san diego', 'la jolla', 'sorrento valley'],
        'Basel': ['basel', 'switzerland'],
        'UK Golden Triangle': [
            'cambridge, uk', 'cambridge uk', 'oxford', 'london',
            'stevenage', 'harwell'
        ],
        'Research Triangle': [
            'research triangle', 'durham', 'raleigh', 'chapel hill',
            'north carolina'
        ],
        'New Jersey': ['new jersey', 'princeton', 'newark'],
        'Seattle': ['seattle', 'bellevue', 'bothell']
    }
    
    def __init__(self):
        """Initialize the location parser."""
        pass
    
    def normalize_location(self, location: str) -> str:
        """
        Normalize location string for comparison.
        
        Args:
            location: Raw location string
            
        Returns:
            Normalized location string
        """
        if not location:
            return ""
        
        # Convert to lowercase and remove extra whitespace
        normalized = location.lower().strip()
        
        # Remove common suffixes
        normalized = re.sub(r',?\s*(area|region)$', '', normalized)
        
        return normalized
    
    def identify_hub(self, location: str) -> Optional[str]:
        """
        Identify if a location is in a biotech hub.
        
        Args:
            location: Location string to check
            
        Returns:
            Hub name if found, None otherwise
        """
        if not location:
            return None
        
        normalized = self.normalize_location(location)
        
        for hub_name, variations in self.BIOTECH_HUBS.items():
            for variation in variations:
                if variation in normalized:
                    return hub_name
        
        return None
    
    def calculate_location_score(self, location: str) -> int:
        """
        Calculate location score based on biotech hub proximity.
        
        Args:
            location: Location string
            
        Returns:
            Score (0-10)
        """
        hub = self.identify_hub(location)
        
        if hub:
            # Major hubs get full score
            if hub in ['Boston/Cambridge', 'San Francisco Bay Area', 'Basel']:
                return 10
            # Secondary hubs get partial score
            else:
                return 7
        
        return 0
    
    def parse_linkedin_location(self, location_str: str) -> Dict[str, str]:
        """
        Parse LinkedIn location format which may contain both person and company location.
        
        Args:
            location_str: Raw location string from LinkedIn
            
        Returns:
            Dictionary with 'person_location' and 'company_hq' keys
        """
        # LinkedIn sometimes shows "Person Location · Company HQ"
        if '·' in location_str or '•' in location_str:
            parts = re.split(r'[·•]', location_str)
            return {
                'person_location': parts[0].strip() if len(parts) > 0 else "",
                'company_hq': parts[1].strip() if len(parts) > 1 else ""
            }
        
        # If no separator, assume it's the person's location
        return {
            'person_location': location_str.strip(),
            'company_hq': ""
        }
    
    def is_remote(self, location: str) -> bool:
        """
        Check if location indicates remote work.
        
        Args:
            location: Location string
            
        Returns:
            True if remote, False otherwise
        """
        remote_keywords = ['remote', 'work from home', 'wfh', 'distributed']
        normalized = self.normalize_location(location)
        
        return any(keyword in normalized for keyword in remote_keywords)
    
    def extract_country(self, location: str) -> Optional[str]:
        """
        Extract country from location string.
        
        Args:
            location: Location string
            
        Returns:
            Country name if found
        """
        # Common country patterns
        countries = {
            'United States': ['usa', 'united states', 'u.s.', 'us'],
            'United Kingdom': ['uk', 'united kingdom', 'england', 'scotland', 'wales'],
            'Switzerland': ['switzerland', 'swiss'],
            'Germany': ['germany', 'deutschland'],
            'France': ['france'],
            'Netherlands': ['netherlands', 'holland'],
            'Belgium': ['belgium'],
            'Canada': ['canada'],
            'China': ['china', 'prc'],
            'Japan': ['japan'],
            'Singapore': ['singapore']
        }
        
        normalized = self.normalize_location(location)
        
        for country, variations in countries.items():
            for variation in variations:
                if variation in normalized:
                    return country
        
        return None


# Example usage
if __name__ == "__main__":
    parser = LocationParser()
    
    # Test cases
    test_locations = [
        "Boston, MA",
        "San Francisco Bay Area",
        "Remote · Cambridge, MA",
        "Basel, Switzerland",
        "New York, NY",
        "Cambridge, UK"
    ]
    
    for loc in test_locations:
        hub = parser.identify_hub(loc)
        score = parser.calculate_location_score(loc)
        parsed = parser.parse_linkedin_location(loc)
        print(f"\nLocation: {loc}")
        print(f"  Hub: {hub}")
        print(f"  Score: {score}")
        print(f"  Parsed: {parsed}")
