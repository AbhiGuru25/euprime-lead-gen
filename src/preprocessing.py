"""
AI Lead Scoring System - Data Preprocessing Module
Handles feature engineering, encoding, and scaling
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import pickle

class LeadPreprocessor:
    """Preprocess lead data for machine learning"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = None
        
    def preprocess(self, df, is_training=True):
        """
        Preprocess lead data
        
        Args:
            df: Input dataframe
            is_training: Whether this is training data (fit encoders) or test data (transform only)
        
        Returns:
            Preprocessed dataframe
        """
        df = df.copy()
        
        # Feature engineering
        df = self._engineer_features(df)
        
        # Encode categorical variables
        categorical_cols = ['industry', 'company_size', 'country', 'source', 
                           'estimated_budget', 'decision_timeline']
        
        for col in categorical_cols:
            if col in df.columns:
                if is_training:
                    le = LabelEncoder()
                    df[f'{col}_encoded'] = le.fit_transform(df[col].astype(str))
                    self.label_encoders[col] = le
                else:
                    if col in self.label_encoders:
                        # Handle unseen categories
                        le = self.label_encoders[col]
                        df[f'{col}_encoded'] = df[col].apply(
                            lambda x: le.transform([str(x)])[0] if str(x) in le.classes_ else -1
                        )
        
        # Select features for modeling
        feature_cols = [
            # Encoded categorical
            'industry_encoded', 'company_size_encoded', 'country_encoded', 
            'source_encoded', 'estimated_budget_encoded', 'decision_timeline_encoded',
            
            # Numerical features
            'website_visits', 'pages_viewed', 'time_on_site_minutes',
            'email_opens', 'email_clicks', 'content_downloads',
            'webinar_attended', 'demo_requested', 'decision_maker_contacted',
            'days_since_first_contact', 'engagement_score', 'fit_score',
            
            # Engineered features
            'engagement_intensity', 'email_engagement_rate', 'visit_depth',
            'total_interactions', 'is_high_budget', 'is_urgent_timeline'
        ]
        
        # Store feature columns for later use
        if is_training:
            self.feature_columns = [col for col in feature_cols if col in df.columns]
        
        return df
    
    def _engineer_features(self, df):
        """Create new features from existing ones"""
        
        # Engagement intensity (interactions per day)
        df['engagement_intensity'] = (
            df['website_visits'] + df['email_opens'] + df['content_downloads']
        ) / (df['days_since_first_contact'] + 1)
        
        # Email engagement rate
        df['email_engagement_rate'] = df['email_clicks'] / (df['email_opens'] + 1)
        
        # Visit depth (pages per visit)
        df['visit_depth'] = df['pages_viewed'] / (df['website_visits'] + 1)
        
        # Total interactions
        df['total_interactions'] = (
            df['website_visits'] + df['email_opens'] + df['email_clicks'] + 
            df['content_downloads'] + df['webinar_attended'] + df['demo_requested']
        )
        
        # Budget flags
        df['is_high_budget'] = df['estimated_budget'].isin(['100K-500K', '500K+']).astype(int)
        
        # Timeline urgency
        df['is_urgent_timeline'] = df['decision_timeline'].isin(['Immediate', '1-3 months']).astype(int)
        
        return df
    
    def get_features_and_target(self, df):
        """Extract feature matrix and target variable"""
        
        if self.feature_columns is None:
            raise ValueError("Preprocessor must be fitted first (call preprocess with is_training=True)")
        
        X = df[self.feature_columns]
        y = df['converted'] if 'converted' in df.columns else None
        
        return X, y
    
    def scale_features(self, X, is_training=True):
        """Scale numerical features"""
        
        if is_training:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = self.scaler.transform(X)
        
        return pd.DataFrame(X_scaled, columns=X.columns, index=X.index)
    
    def save(self, filepath='models/preprocessor.pkl'):
        """Save preprocessor state"""
        with open(filepath, 'wb') as f:
            pickle.dump({
                'scaler': self.scaler,
                'label_encoders': self.label_encoders,
                'feature_columns': self.feature_columns
            }, f)
        print(f"✓ Preprocessor saved to {filepath}")
    
    def load(self, filepath='models/preprocessor.pkl'):
        """Load preprocessor state"""
        with open(filepath, 'rb') as f:
            state = pickle.load(f)
            self.scaler = state['scaler']
            self.label_encoders = state['label_encoders']
            self.feature_columns = state['feature_columns']
        print(f"✓ Preprocessor loaded from {filepath}")


def prepare_train_test_split(df, test_size=0.2, random_state=42):
    """Prepare train-test split"""
    
    preprocessor = LeadPreprocessor()
    
    # Preprocess
    df_processed = preprocessor.preprocess(df, is_training=True)
    
    # Get features and target
    X, y = preprocessor.get_features_and_target(df_processed)
    
    # Scale features
    X_scaled = preprocessor.scale_features(X, is_training=True)
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    return X_train, X_test, y_train, y_test, preprocessor


if __name__ == '__main__':
    # Test preprocessing
    df = pd.read_csv('data/sample_leads.csv')
    
    X_train, X_test, y_train, y_test, preprocessor = prepare_train_test_split(df)
    
    print("Preprocessing complete!")
    print(f"Training set: {X_train.shape}")
    print(f"Test set: {X_test.shape}")
    print(f"\nFeatures: {preprocessor.feature_columns}")
