"""
AI Lead Scoring System - Prediction Engine
Loads trained models and makes predictions on new data
"""

import pandas as pd
import numpy as np
import pickle
import sys
sys.path.append('.')

from src.preprocessing import LeadPreprocessor

class LeadScorePredictor:
    """Prediction engine for lead scoring"""
    
    def __init__(self):
        self.scorer = None
        self.segmenter = None
        self.preprocessor = None
        self.segment_names = {
            0: 'High-Value Prospects',
            1: 'Engaged Explorers',
            2: 'Cold Leads',
            3: 'Nurture Candidates'
        }
        
    def load_models(self):
        """Load all trained models"""
        try:
            # Load preprocessor
            with open('models/preprocessor.pkl', 'rb') as f:
                state = pickle.load(f)
                self.preprocessor = LeadPreprocessor()
                self.preprocessor.scaler = state['scaler']
                self.preprocessor.label_encoders = state['label_encoders']
                self.preprocessor.feature_columns = state['feature_columns']
            
            # Load lead scorer
            with open('models/lead_scorer.pkl', 'rb') as f:
                self.scorer = pickle.load(f)
            
            # Load segmenter
            with open('models/customer_segmenter.pkl', 'rb') as f:
                self.segmenter = pickle.load(f)
            
            print("✓ All models loaded successfully")
            return True
            
        except Exception as e:
            print(f"Error loading models: {e}")
            return False
    
    def predict(self, df):
        """
        Make predictions on new lead data
        
        Args:
            df: DataFrame with lead data
            
        Returns:
            DataFrame with predictions
        """
        if self.scorer is None or self.preprocessor is None:
            raise ValueError("Models not loaded. Call load_models() first.")
        
        # Store original data
        df_original = df.copy()
        
        # Preprocess
        df_processed = self.preprocessor.preprocess(df, is_training=False)
        
        # Get features
        X, _ = self.preprocessor.get_features_and_target(df_processed)
        
        # Scale
        X_scaled = self.preprocessor.scale_features(X, is_training=False)
        
        # Predict conversion probability
        conversion_prob = self.scorer.predict_proba(X_scaled)[:, 1]
        
        # Convert to 0-100 score
        lead_scores = (conversion_prob * 100).round(2)
        
        # Predict segments
        segments = self.segmenter.predict(X_scaled)
        segment_names = [self.segment_names.get(s, f'Segment {s}') for s in segments]
        
        # Predict conversion class
        conversion_pred = self.scorer.predict(X_scaled)
        
        # Add predictions to original dataframe
        df_result = df_original.copy()
        df_result['lead_score'] = lead_scores
        df_result['conversion_probability'] = (conversion_prob * 100).round(2)
        df_result['predicted_conversion'] = conversion_pred
        df_result['customer_segment'] = segment_names
        df_result['segment_id'] = segments
        
        # Add priority level based on score
        df_result['priority'] = pd.cut(
            lead_scores,
            bins=[0, 30, 60, 80, 100],
            labels=['Low', 'Medium', 'High', 'Critical']
        )
        
        return df_result
    
    def get_top_leads(self, df_predictions, n=10):
        """Get top N leads by score"""
        return df_predictions.nlargest(n, 'lead_score')
    
    def get_segment_summary(self, df_predictions):
        """Get summary statistics by segment"""
        summary = df_predictions.groupby('customer_segment').agg({
            'lead_score': ['count', 'mean', 'min', 'max'],
            'conversion_probability': 'mean'
        }).round(2)
        
        return summary


def predict_from_csv(input_file, output_file=None):
    """
    Predict lead scores from CSV file
    
    Args:
        input_file: Path to input CSV
        output_file: Path to save predictions (optional)
    """
    # Load data
    df = pd.read_csv(input_file)
    print(f"Loaded {len(df)} leads from {input_file}")
    
    # Initialize predictor
    predictor = LeadScorePredictor()
    predictor.load_models()
    
    # Make predictions
    df_predictions = predictor.predict(df)
    
    # Display summary
    print("\n" + "="*60)
    print("PREDICTION SUMMARY")
    print("="*60)
    print(f"Total Leads: {len(df_predictions)}")
    print(f"Average Lead Score: {df_predictions['lead_score'].mean():.2f}")
    print(f"Predicted Conversions: {df_predictions['predicted_conversion'].sum()}")
    print(f"Predicted Conversion Rate: {df_predictions['predicted_conversion'].mean()*100:.2f}%")
    
    print("\nTop 5 Leads:")
    print(predictor.get_top_leads(df_predictions, 5)[['lead_id', 'company_name', 'lead_score', 
                                                        'customer_segment', 'priority']].to_string(index=False))
    
    print("\nSegment Distribution:")
    print(df_predictions['customer_segment'].value_counts())
    
    # Save if output file specified
    if output_file:
        df_predictions.to_csv(output_file, index=False)
        print(f"\n✓ Predictions saved to {output_file}")
    
    return df_predictions


if __name__ == '__main__':
    # Test predictions
    df_predictions = predict_from_csv('data/sample_leads.csv', 'data/predictions.csv')
