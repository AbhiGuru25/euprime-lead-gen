"""
AI Lead Scoring System - Google Sheets Integration
Exports predictions to Google Sheets for easy sharing
"""

import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json
import os

class GoogleSheetsExporter:
    """Export lead scoring results to Google Sheets"""
    
    def __init__(self, credentials_file='config/credentials.json'):
        self.credentials_file = credentials_file
        self.client = None
        self.sheet = None
        
    def authenticate(self):
        """Authenticate with Google Sheets API"""
        try:
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            if not os.path.exists(self.credentials_file):
                print(f"⚠ Credentials file not found: {self.credentials_file}")
                print("Please set up Google Sheets API credentials.")
                return False
            
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                self.credentials_file, scope
            )
            self.client = gspread.authorize(creds)
            print("✓ Google Sheets authentication successful")
            return True
            
        except Exception as e:
            print(f"Authentication error: {e}")
            return False
    
    def create_spreadsheet(self, title=None):
        """Create a new Google Spreadsheet"""
        if title is None:
            title = f"Lead Scoring Results - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        try:
            self.sheet = self.client.create(title)
            print(f"✓ Created spreadsheet: {title}")
            
            # Make it shareable
            self.sheet.share('', perm_type='anyone', role='reader')
            
            return self.sheet
            
        except Exception as e:
            print(f"Error creating spreadsheet: {e}")
            return None
    
    def export_predictions(self, df_predictions, sheet_name='Lead Scores'):
        """
        Export predictions to Google Sheets
        
        Args:
            df_predictions: DataFrame with predictions
            sheet_name: Name of the worksheet
        """
        if self.client is None:
            if not self.authenticate():
                print("Cannot export without authentication")
                return None
        
        # Create spreadsheet if not exists
        if self.sheet is None:
            self.create_spreadsheet()
        
        try:
            # Select or create worksheet
            try:
                worksheet = self.sheet.worksheet(sheet_name)
            except:
                worksheet = self.sheet.add_worksheet(title=sheet_name, rows=1000, cols=20)
            
            # Prepare data for export
            export_cols = [
                'lead_id', 'company_name', 'industry', 'company_size', 'country',
                'lead_score', 'conversion_probability', 'customer_segment', 'priority',
                'website_visits', 'email_opens', 'demo_requested', 'estimated_budget',
                'decision_timeline'
            ]
            
            # Filter columns that exist
            export_cols = [col for col in export_cols if col in df_predictions.columns]
            df_export = df_predictions[export_cols].copy()
            
            # Sort by lead score
            df_export = df_export.sort_values('lead_score', ascending=False)
            
            # Convert to list of lists
            data = [df_export.columns.tolist()] + df_export.values.tolist()
            
            # Clear and update worksheet
            worksheet.clear()
            worksheet.update('A1', data)
            
            # Format header row
            worksheet.format('A1:Z1', {
                'backgroundColor': {'red': 0.2, 'green': 0.4, 'blue': 0.8},
                'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}},
                'horizontalAlignment': 'CENTER'
            })
            
            # Auto-resize columns
            worksheet.columns_auto_resize(0, len(export_cols))
            
            print(f"✓ Exported {len(df_export)} leads to Google Sheets")
            
            # Get shareable link
            url = self.sheet.url
            print(f"\n📊 Shareable Link: {url}")
            
            return url
            
        except Exception as e:
            print(f"Error exporting to Google Sheets: {e}")
            return None
    
    def export_summary(self, df_predictions, sheet_name='Summary'):
        """Export summary statistics"""
        if self.sheet is None:
            return
        
        try:
            # Create summary data
            summary_data = [
                ['Lead Scoring Summary', ''],
                ['Generated', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                ['', ''],
                ['Total Leads', len(df_predictions)],
                ['Average Lead Score', f"{df_predictions['lead_score'].mean():.2f}"],
                ['Predicted Conversions', df_predictions['predicted_conversion'].sum()],
                ['Predicted Conversion Rate', f"{df_predictions['predicted_conversion'].mean()*100:.2f}%"],
                ['', ''],
                ['Priority Distribution', ''],
            ]
            
            # Add priority counts
            priority_counts = df_predictions['priority'].value_counts().to_dict()
            for priority, count in priority_counts.items():
                summary_data.append([f'  {priority}', count])
            
            summary_data.append(['', ''])
            summary_data.append(['Segment Distribution', ''])
            
            # Add segment counts
            segment_counts = df_predictions['customer_segment'].value_counts().to_dict()
            for segment, count in segment_counts.items():
                summary_data.append([f'  {segment}', count])
            
            # Create or get worksheet
            try:
                worksheet = self.sheet.worksheet(sheet_name)
            except:
                worksheet = self.sheet.add_worksheet(title=sheet_name, rows=100, cols=10)
            
            # Update worksheet
            worksheet.clear()
            worksheet.update('A1', summary_data)
            
            # Format title
            worksheet.format('A1:B1', {
                'textFormat': {'bold': True, 'fontSize': 14},
                'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
            })
            
            print(f"✓ Summary exported to sheet: {sheet_name}")
            
        except Exception as e:
            print(f"Error exporting summary: {e}")


def export_to_sheets(df_predictions, credentials_file='config/credentials.json'):
    """
    Convenience function to export predictions to Google Sheets
    
    Args:
        df_predictions: DataFrame with predictions
        credentials_file: Path to Google API credentials
    
    Returns:
        Shareable URL or None
    """
    exporter = GoogleSheetsExporter(credentials_file)
    
    if not exporter.authenticate():
        print("\n⚠ Google Sheets export skipped (no credentials)")
        print("To enable Google Sheets integration:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a project and enable Google Sheets API")
        print("3. Create service account credentials")
        print("4. Download JSON and save to config/credentials.json")
        return None
    
    # Export predictions
    url = exporter.export_predictions(df_predictions, 'Lead Scores')
    
    # Export summary
    exporter.export_summary(df_predictions, 'Summary')
    
    return url


if __name__ == '__main__':
    # Test export
    import sys
    sys.path.append('.')
    from src.predictor import predict_from_csv
    
    # Get predictions
    df_predictions = predict_from_csv('data/sample_leads.csv')
    
    # Export to Google Sheets
    url = export_to_sheets(df_predictions)
    
    if url:
        print(f"\n✓ Data exported successfully!")
        print(f"View at: {url}")
