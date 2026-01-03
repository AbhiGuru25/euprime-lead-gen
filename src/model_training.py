"""
AI Lead Scoring System - Model Training Module
Trains lead scoring and customer segmentation models
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report
import pickle
import sys
sys.path.append('.')

from src.data_generator import LeadDataGenerator
from src.preprocessing import prepare_train_test_split

class LeadScoringModel:
    """Lead scoring model using Random Forest"""
    
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        self.feature_importance = None
        
    def train(self, X_train, y_train):
        """Train the model"""
        print("Training Lead Scoring Model...")
        self.model.fit(X_train, y_train)
        self.feature_importance = pd.DataFrame({
            'feature': X_train.columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        print("✓ Model training complete")
        
    def predict(self, X):
        """Predict conversion probability"""
        return self.model.predict_proba(X)[:, 1]
    
    def predict_class(self, X):
        """Predict conversion class"""
        return self.model.predict(X)
    
    def evaluate(self, X_test, y_test):
        """Evaluate model performance"""
        y_pred = self.predict_class(X_test)
        y_prob = self.predict(X_test)
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred),
            'roc_auc': roc_auc_score(y_test, y_prob)
        }
        
        print("\n" + "="*50)
        print("MODEL EVALUATION METRICS")
        print("="*50)
        for metric, value in metrics.items():
            print(f"{metric.upper():15s}: {value:.4f}")
        print("="*50)
        
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Not Converted', 'Converted']))
        
        return metrics
    
    def save(self, filepath='models/lead_scorer.pkl'):
        """Save model"""
        with open(filepath, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"✓ Model saved to {filepath}")
    
    def load(self, filepath='models/lead_scorer.pkl'):
        """Load model"""
        with open(filepath, 'rb') as f:
            self.model = pickle.load(f)
        print(f"✓ Model loaded from {filepath}")


class CustomerSegmentationModel:
    """Customer segmentation using K-Means clustering"""
    
    def __init__(self, n_clusters=4):
        self.model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.n_clusters = n_clusters
        self.segment_names = {
            0: 'High-Value Prospects',
            1: 'Engaged Explorers',
            2: 'Cold Leads',
            3: 'Nurture Candidates'
        }
        
    def train(self, X_train):
        """Train clustering model"""
        print(f"\nTraining Customer Segmentation Model ({self.n_clusters} segments)...")
        self.model.fit(X_train)
        print("✓ Segmentation model training complete")
        
    def predict(self, X):
        """Predict customer segment"""
        return self.model.predict(X)
    
    def get_segment_name(self, segment_id):
        """Get human-readable segment name"""
        return self.segment_names.get(segment_id, f'Segment {segment_id}')
    
    def save(self, filepath='models/customer_segmenter.pkl'):
        """Save model"""
        with open(filepath, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"✓ Segmentation model saved to {filepath}")
    
    def load(self, filepath='models/customer_segmenter.pkl'):
        """Load model"""
        with open(filepath, 'rb') as f:
            self.model = pickle.load(f)
        print(f"✓ Segmentation model loaded from {filepath}")


def train_all_models():
    """Complete training pipeline"""
    
    print("\n" + "="*60)
    print("AI LEAD SCORING SYSTEM - MODEL TRAINING PIPELINE")
    print("="*60 + "\n")
    
    # Step 1: Generate data
    print("Step 1: Generating synthetic lead data...")
    generator = LeadDataGenerator(n_samples=1000)
    df = generator.save_to_csv('data/sample_leads.csv')
    
    # Step 2: Preprocess and split
    print("\nStep 2: Preprocessing and splitting data...")
    X_train, X_test, y_train, y_test, preprocessor = prepare_train_test_split(df)
    preprocessor.save('models/preprocessor.pkl')
    
    # Step 3: Train lead scoring model
    print("\nStep 3: Training Lead Scoring Model...")
    scorer = LeadScoringModel()
    scorer.train(X_train, y_train)
    
    # Step 4: Evaluate
    print("\nStep 4: Evaluating model...")
    metrics = scorer.evaluate(X_test, y_test)
    
    # Step 5: Save lead scoring model
    scorer.save('models/lead_scorer.pkl')
    
    # Step 6: Train segmentation model
    print("\nStep 5: Training Customer Segmentation Model...")
    segmenter = CustomerSegmentationModel(n_clusters=4)
    segmenter.train(X_train)
    segmenter.save('models/customer_segmenter.pkl')
    
    # Step 7: Display feature importance
    print("\n" + "="*50)
    print("TOP 10 MOST IMPORTANT FEATURES")
    print("="*50)
    print(scorer.feature_importance.head(10).to_string(index=False))
    print("="*50)
    
    print("\n✓ All models trained and saved successfully!")
    print("\nModel files created:")
    print("  - models/lead_scorer.pkl")
    print("  - models/customer_segmenter.pkl")
    print("  - models/preprocessor.pkl")
    
    return scorer, segmenter, preprocessor, metrics


if __name__ == '__main__':
    train_all_models()
