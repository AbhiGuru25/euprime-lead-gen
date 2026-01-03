"""
Lead scoring engine that calculates propensity-to-buy scores based on
multiple weighted criteria.
"""

from typing import Dict, List, Optional
import yaml
import os
from datetime import datetime, timedelta
from src.location_parser import LocationParser


class LeadScorer:
    """Calculate propensity-to-buy scores for leads."""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize the lead scorer.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.weights = self.config['scoring']
        self.job_titles = self.config['keywords']['job_titles']
        self.location_parser = LocationParser()
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def calculate_role_fit_score(self, title: str) -> int:
        """
        Calculate role fit score based on job title.
        
        Args:
            title: Job title string
            
        Returns:
            Score (0-30)
        """
        if not title:
            return 0
        
        title_lower = title.lower()
        
        # High-value keywords
        high_value_keywords = [
            'director', 'head', 'vp', 'vice president', 'chief',
            'toxicology', 'safety', 'preclinical'
        ]
        
        # Medium-value keywords
        medium_value_keywords = [
            'manager', 'lead', 'senior', 'principal',
            'hepatic', 'liver', 'dili', '3d'
        ]
        
        # Low-value keywords
        low_value_keywords = [
            'scientist', 'researcher', 'associate'
        ]
        
        # Count keyword matches
        high_matches = sum(1 for kw in high_value_keywords if kw in title_lower)
        medium_matches = sum(1 for kw in medium_value_keywords if kw in title_lower)
        low_matches = sum(1 for kw in low_value_keywords if kw in title_lower)
        
        # Calculate score
        if high_matches >= 2:
            return 30  # Perfect match (e.g., "Director of Toxicology")
        elif high_matches == 1 and medium_matches >= 1:
            return 25  # Strong match
        elif high_matches == 1:
            return 20  # Good match
        elif medium_matches >= 2:
            return 15  # Moderate match
        elif medium_matches == 1 or low_matches >= 1:
            return 10  # Weak match
        
        return 0
    
    def calculate_company_intent_score(self, funding_info: Optional[Dict]) -> int:
        """
        Calculate company intent score based on funding.
        
        Args:
            funding_info: Dictionary with 'round', 'amount', 'date' keys
            
        Returns:
            Score (0-20)
        """
        if not funding_info:
            return 0
        
        funding_round = funding_info.get('round', '').lower()
        funding_date = funding_info.get('date')
        
        # Recent funding (within last 12 months) is more valuable
        is_recent = False
        if funding_date:
            try:
                if isinstance(funding_date, str):
                    funding_date = datetime.fromisoformat(funding_date)
                is_recent = funding_date > datetime.now() - timedelta(days=365)
            except:
                pass
        
        # Score based on funding round
        if 'series c' in funding_round or 'series d' in funding_round:
            base_score = 20
        elif 'series b' in funding_round:
            base_score = 18
        elif 'series a' in funding_round:
            base_score = 15
        elif 'seed' in funding_round:
            base_score = 10
        elif 'ipo' in funding_round or 'public' in funding_round:
            base_score = 20
        else:
            base_score = 5
        
        # Bonus for recent funding
        if is_recent:
            base_score = min(20, base_score + 5)
        
        return base_score
    
    def calculate_technographic_score(self, company_description: str) -> int:
        """
        Calculate technographic score based on company's existing tech use.
        
        Args:
            company_description: Company description or about text
            
        Returns:
            Score (0-15)
        """
        if not company_description:
            return 0
        
        desc_lower = company_description.lower()
        
        # Keywords indicating use of similar technology
        tech_keywords = [
            'in vitro', 'in-vitro', '3d model', 'organoid', 'spheroid',
            'organ-on-chip', 'microphysiological', 'cell culture',
            'drug discovery', 'preclinical', 'toxicology'
        ]
        
        matches = sum(1 for kw in tech_keywords if kw in desc_lower)
        
        if matches >= 4:
            return 15
        elif matches == 3:
            return 12
        elif matches == 2:
            return 8
        elif matches == 1:
            return 5
        
        return 0
    
    def calculate_location_score(self, location: str) -> int:
        """
        Calculate location score based on biotech hub proximity.
        
        Args:
            location: Location string
            
        Returns:
            Score (0-10)
        """
        return self.location_parser.calculate_location_score(location)
    
    def calculate_scientific_intent_score(self, publications: List[Dict]) -> int:
        """
        Calculate scientific intent score based on recent publications.
        
        Args:
            publications: List of publication dictionaries with 'title', 'date', 'keywords'
            
        Returns:
            Score (0-40)
        """
        if not publications:
            return 0
        
        # Keywords indicating relevant research
        relevant_keywords = [
            'dili', 'drug-induced liver injury', 'hepatotoxicity',
            'liver toxicity', '3d', 'spheroid', 'organoid',
            'in vitro', 'hepatocyte', 'liver model'
        ]
        
        score = 0
        recent_cutoff = datetime.now() - timedelta(days=730)  # 2 years
        
        for pub in publications:
            pub_date = pub.get('date')
            pub_title = pub.get('title', '').lower()
            pub_abstract = pub.get('abstract', '').lower()
            
            # Check if publication is recent
            is_recent = False
            if pub_date:
                try:
                    if isinstance(pub_date, str):
                        pub_date = datetime.fromisoformat(pub_date)
                    is_recent = pub_date > recent_cutoff
                except:
                    pass
            
            # Count keyword matches
            text = pub_title + ' ' + pub_abstract
            matches = sum(1 for kw in relevant_keywords if kw in text)
            
            # Score this publication
            if matches >= 3 and is_recent:
                score += 20  # Highly relevant recent publication
            elif matches >= 2 and is_recent:
                score += 15
            elif matches >= 1 and is_recent:
                score += 10
            elif matches >= 2:
                score += 8  # Relevant but older
            elif matches >= 1:
                score += 5
        
        # Cap at maximum score
        return min(40, score)
    
    def calculate_total_score(self, lead_data: Dict) -> Dict:
        """
        Calculate total propensity-to-buy score for a lead.
        
        Args:
            lead_data: Dictionary containing all lead information
            
        Returns:
            Dictionary with individual scores and total score
        """
        scores = {
            'role_fit': self.calculate_role_fit_score(lead_data.get('title', '')),
            'company_intent': self.calculate_company_intent_score(lead_data.get('funding_info')),
            'technographic': self.calculate_technographic_score(lead_data.get('company_description', '')),
            'location': self.calculate_location_score(lead_data.get('location', '')),
            'scientific_intent': self.calculate_scientific_intent_score(lead_data.get('publications', []))
        }
        
        # Calculate total (max 115, but we'll normalize to 100)
        total_raw = sum(scores.values())
        total_normalized = min(100, int((total_raw / 115) * 100))
        
        scores['total'] = total_normalized
        scores['total_raw'] = total_raw
        
        return scores


# Example usage
if __name__ == "__main__":
    scorer = LeadScorer()
    
    # Test case 1: High-scoring lead
    high_score_lead = {
        'name': 'Dr. Jane Smith',
        'title': 'Director of Toxicology',
        'company': 'BioTech Inc',
        'location': 'Cambridge, MA',
        'company_description': 'Leading drug discovery company using 3D in vitro models and organ-on-chip technology for preclinical safety assessment',
        'funding_info': {
            'round': 'Series B',
            'amount': 50000000,
            'date': '2025-06-15'
        },
        'publications': [
            {
                'title': 'Novel 3D hepatic spheroid models for DILI prediction',
                'date': '2025-03-01',
                'abstract': 'We developed advanced 3D liver models for drug-induced liver injury assessment'
            }
        ]
    }
    
    # Test case 2: Low-scoring lead
    low_score_lead = {
        'name': 'John Doe',
        'title': 'Research Assistant',
        'company': 'Small Lab',
        'location': 'Austin, TX',
        'company_description': 'General biology research',
        'funding_info': None,
        'publications': []
    }
    
    print("High-scoring lead:")
    high_scores = scorer.calculate_total_score(high_score_lead)
    for key, value in high_scores.items():
        print(f"  {key}: {value}")
    
    print("\nLow-scoring lead:")
    low_scores = scorer.calculate_total_score(low_score_lead)
    for key, value in low_scores.items():
        print(f"  {key}: {value}")
