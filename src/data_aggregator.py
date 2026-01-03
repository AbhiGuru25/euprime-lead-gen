"""
Data aggregator to combine data from multiple sources, deduplicate,
and calculate final scores for all leads.
"""

import pandas as pd
from typing import List, Dict
import logging
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.lead_scorer import LeadScorer
from src.location_parser import LocationParser
from src.email_finder import EmailFinder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataAggregator:
    """Aggregate and score leads from multiple data sources."""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        Initialize the data aggregator.
        
        Args:
            config_path: Path to configuration file
        """
        self.scorer = LeadScorer(config_path)
        self.location_parser = LocationParser()
        self.email_finder = EmailFinder()
        
    def deduplicate_leads(self, leads: List[Dict]) -> List[Dict]:
        """
        Deduplicate leads based on name and company.
        
        Args:
            leads: List of lead dictionaries
            
        Returns:
            Deduplicated list of leads
        """
        seen = set()
        unique_leads = []
        
        for lead in leads:
            # Create unique key from name and company
            key = (
                lead.get('name', '').lower().strip(),
                lead.get('company', '').lower().strip()
            )
            
            if key not in seen and key[0] and key[1]:
                seen.add(key)
                unique_leads.append(lead)
        
        logger.info(f"Deduplicated {len(leads)} leads to {len(unique_leads)} unique leads")
        return unique_leads
    
    def enrich_lead(self, lead: Dict) -> Dict:
        """
        Enrich a single lead with additional data.
        
        Args:
            lead: Lead dictionary
            
        Returns:
            Enriched lead dictionary
        """
        # Parse location if needed
        if 'person_location' not in lead and 'location' in lead:
            parsed_location = self.location_parser.parse_linkedin_location(lead['location'])
            lead['person_location'] = parsed_location['person_location']
            lead['company_hq'] = parsed_location['company_hq']
        
        # Generate email if not present
        if 'email' not in lead or not lead['email']:
            lead['email'] = self.email_finder.find_most_likely_email(
                lead.get('name', ''),
                lead.get('company', ''),
                lead.get('email_domain')
            )
        
        # Identify biotech hub
        location_to_check = lead.get('company_hq') or lead.get('person_location', '')
        lead['biotech_hub'] = self.location_parser.identify_hub(location_to_check)
        
        return lead
    
    def score_lead(self, lead: Dict) -> Dict:
        """
        Calculate scores for a single lead.
        
        Args:
            lead: Lead dictionary
            
        Returns:
            Lead dictionary with scores added
        """
        # Prepare data for scoring
        scoring_data = {
            'title': lead.get('title', ''),
            'location': lead.get('company_hq') or lead.get('person_location', ''),
            'company_description': lead.get('company_description', ''),
            'funding_info': None,
            'publications': []
        }
        
        # Add funding info if available
        if lead.get('funding_round'):
            scoring_data['funding_info'] = {
                'round': lead.get('funding_round', ''),
                'amount': lead.get('funding_amount'),
                'date': lead.get('funding_date')
            }
        
        # Add publications if available
        if lead.get('publications') and isinstance(lead['publications'], list):
            scoring_data['publications'] = lead['publications']
        elif lead.get('recent_dili_paper'):
            # Create a dummy publication for scoring
            scoring_data['publications'] = [{
                'title': 'DILI research',
                'date': '2025-01-01',
                'abstract': 'drug-induced liver injury 3D model'
            }] * lead.get('publications', 1)
        
        # Calculate scores
        scores = self.scorer.calculate_total_score(scoring_data)
        
        # Add scores to lead
        lead['score_role_fit'] = scores['role_fit']
        lead['score_company_intent'] = scores['company_intent']
        lead['score_technographic'] = scores['technographic']
        lead['score_location'] = scores['location']
        lead['score_scientific_intent'] = scores['scientific_intent']
        lead['score_total'] = scores['total']
        
        return lead
    
    def process_leads(self, leads: List[Dict]) -> pd.DataFrame:
        """
        Process all leads: deduplicate, enrich, and score.
        
        Args:
            leads: List of lead dictionaries
            
        Returns:
            DataFrame with processed and scored leads
        """
        logger.info(f"Processing {len(leads)} leads...")
        
        # Deduplicate
        unique_leads = self.deduplicate_leads(leads)
        
        # Enrich and score each lead
        processed_leads = []
        for lead in unique_leads:
            try:
                enriched = self.enrich_lead(lead)
                scored = self.score_lead(enriched)
                processed_leads.append(scored)
            except Exception as e:
                logger.error(f"Error processing lead {lead.get('name')}: {str(e)}")
                continue
        
        # Convert to DataFrame
        df = pd.DataFrame(processed_leads)
        
        # Sort by total score (descending)
        if 'score_total' in df.columns:
            df = df.sort_values('score_total', ascending=False).reset_index(drop=True)
            df['rank'] = range(1, len(df) + 1)
        
        logger.info(f"Successfully processed {len(df)} leads")
        return df
    
    def export_to_csv(self, df: pd.DataFrame, filename: str = "data/leads_output.csv"):
        """
        Export leads to CSV file.
        
        Args:
            df: DataFrame with leads
            filename: Output filename
        """
        # Select and order columns for export
        export_columns = [
            'rank', 'score_total', 'name', 'title', 'company',
            'person_location', 'company_hq', 'email', 'linkedin',
            'biotech_hub', 'score_role_fit', 'score_company_intent',
            'score_technographic', 'score_location', 'score_scientific_intent'
        ]
        
        # Only include columns that exist
        available_columns = [col for col in export_columns if col in df.columns]
        
        df[available_columns].to_csv(filename, index=False)
        logger.info(f"Exported {len(df)} leads to {filename}")


# Example usage
if __name__ == "__main__":
    from src.sample_data import SAMPLE_LEADS
    
    aggregator = DataAggregator()
    
    # Process sample leads
    df = aggregator.process_leads(SAMPLE_LEADS)
    
    print(f"\nProcessed {len(df)} leads")
    print("\nTop 5 leads:")
    print(df[['rank', 'score_total', 'name', 'title', 'company', 'person_location']].head())
    
    print("\nScore breakdown for top lead:")
    top_lead = df.iloc[0]
    print(f"Name: {top_lead['name']}")
    print(f"Title: {top_lead['title']}")
    print(f"Company: {top_lead['company']}")
    print(f"  Role Fit: {top_lead['score_role_fit']}/30")
    print(f"  Company Intent: {top_lead['score_company_intent']}/20")
    print(f"  Technographic: {top_lead['score_technographic']}/15")
    print(f"  Location: {top_lead['score_location']}/10")
    print(f"  Scientific Intent: {top_lead['score_scientific_intent']}/40")
    print(f"  TOTAL: {top_lead['score_total']}/100")
    
    # Export to CSV
    aggregator.export_to_csv(df)
