"""
AI Lead Scoring System - Data Generator Module
Generates realistic synthetic lead data for training and demonstration
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class LeadDataGenerator:
    """Generate synthetic lead data with realistic features"""
    
    def __init__(self, n_samples=1000, random_state=42):
        self.n_samples = n_samples
        np.random.seed(random_state)
        random.seed(random_state)
        
        # Define realistic categories
        self.industries = ['Technology', 'Healthcare', 'Finance', 'Retail', 'Manufacturing', 
                          'Education', 'Real Estate', 'Consulting', 'E-commerce', 'Media']
        self.company_sizes = ['1-10', '11-50', '51-200', '201-500', '501-1000', '1000+']
        self.countries = ['USA', 'UK', 'Canada', 'Germany', 'France', 'India', 'Australia', 
                         'Singapore', 'UAE', 'Netherlands']
        self.sources = ['Website', 'LinkedIn', 'Email Campaign', 'Referral', 'Trade Show', 
                       'Google Ads', 'Content Download', 'Webinar', 'Cold Outreach']
        
    def generate_leads(self):
        """Generate complete lead dataset"""
        
        data = {
            'lead_id': [f'LEAD_{i:05d}' for i in range(1, self.n_samples + 1)],
            'company_name': [f'Company_{i}' for i in range(1, self.n_samples + 1)],
            'industry': np.random.choice(self.industries, self.n_samples),
            'company_size': np.random.choice(self.company_sizes, self.n_samples),
            'country': np.random.choice(self.countries, self.n_samples),
            'source': np.random.choice(self.sources, self.n_samples),
            
            # Engagement metrics
            'website_visits': np.random.poisson(5, self.n_samples),
            'pages_viewed': np.random.poisson(10, self.n_samples),
            'time_on_site_minutes': np.random.exponential(8, self.n_samples),
            'email_opens': np.random.poisson(3, self.n_samples),
            'email_clicks': np.random.poisson(1, self.n_samples),
            'content_downloads': np.random.poisson(1, self.n_samples),
            'webinar_attended': np.random.choice([0, 1], self.n_samples, p=[0.7, 0.3]),
            'demo_requested': np.random.choice([0, 1], self.n_samples, p=[0.8, 0.2]),
            
            # Firmographic data
            'estimated_budget': np.random.choice(['<10K', '10K-50K', '50K-100K', '100K-500K', '500K+'], 
                                                self.n_samples, p=[0.3, 0.3, 0.2, 0.15, 0.05]),
            'decision_timeline': np.random.choice(['Immediate', '1-3 months', '3-6 months', '6-12 months', 'No timeline'], 
                                                 self.n_samples, p=[0.1, 0.25, 0.3, 0.25, 0.1]),
            'decision_maker_contacted': np.random.choice([0, 1], self.n_samples, p=[0.6, 0.4]),
            
            # Behavioral scores
            'engagement_score': np.random.uniform(0, 100, self.n_samples),
            'fit_score': np.random.uniform(0, 100, self.n_samples),
        }
        
        df = pd.DataFrame(data)
        
        # Add days_since_first_contact
        df['days_since_first_contact'] = np.random.randint(1, 180, self.n_samples)
        
        # Generate conversion label based on features (realistic correlation)
        df['converted'] = self._generate_conversion_labels(df)
        
        # Round numerical columns
        df['time_on_site_minutes'] = df['time_on_site_minutes'].round(2)
        df['engagement_score'] = df['engagement_score'].round(2)
        df['fit_score'] = df['fit_score'].round(2)
        
        return df
    
    def _generate_conversion_labels(self, df):
        """Generate realistic conversion labels based on features"""
        
        # Calculate conversion probability based on multiple factors
        conversion_prob = np.zeros(len(df))
        
        # Engagement factors
        conversion_prob += (df['website_visits'] > 5).astype(int) * 0.1
        conversion_prob += (df['email_opens'] > 3).astype(int) * 0.1
        conversion_prob += df['demo_requested'] * 0.3
        conversion_prob += df['webinar_attended'] * 0.15
        conversion_prob += (df['content_downloads'] > 1).astype(int) * 0.1
        
        # Firmographic factors
        conversion_prob += df['decision_maker_contacted'] * 0.15
        conversion_prob += (df['estimated_budget'].isin(['100K-500K', '500K+'])).astype(int) * 0.1
        conversion_prob += (df['decision_timeline'].isin(['Immediate', '1-3 months'])).astype(int) * 0.15
        
        # Company size factor
        conversion_prob += (df['company_size'].isin(['201-500', '501-1000', '1000+'])).astype(int) * 0.1
        
        # Add some randomness
        conversion_prob += np.random.uniform(-0.2, 0.2, len(df))
        
        # Clip to [0, 1] and generate binary labels
        conversion_prob = np.clip(conversion_prob, 0, 1)
        converted = (np.random.random(len(df)) < conversion_prob).astype(int)
        
        return converted
    
    def save_to_csv(self, filepath='data/sample_leads.csv'):
        """Generate and save lead data to CSV"""
        df = self.generate_leads()
        df.to_csv(filepath, index=False)
        print(f"✓ Generated {len(df)} leads and saved to {filepath}")
        print(f"  Conversion rate: {df['converted'].mean()*100:.2f}%")
        return df


if __name__ == '__main__':
    # Generate sample data
    generator = LeadDataGenerator(n_samples=1000)
    df = generator.save_to_csv('data/sample_leads.csv')
    
    print("\nDataset Summary:")
    print(df.head())
    print(f"\nShape: {df.shape}")
    print(f"\nColumns: {list(df.columns)}")
