# EuPrime AI Lead Generation Tool 🎯

AI-powered lead generation and scoring system for EuPrime's 3D in-vitro models business.

## Overview

This tool identifies, enriches, and ranks qualified leads for 3D in-vitro models used in drug therapy research. It uses a sophisticated **Propensity-to-Buy Scoring System** that analyzes multiple data sources to prioritize the most promising prospects.

## Features

- 🔍 **Multi-Source Data Collection**: Scrapes PubMed, LinkedIn, funding databases, and conference listings
- 🎯 **AI-Powered Scoring**: Weighted scoring algorithm (0-100 scale) based on 5 key criteria
- 📊 **Interactive Dashboard**: Streamlit-based UI with search, filter, and export capabilities
- 📈 **Analytics**: Visual insights into lead distribution and scoring patterns
- 📥 **Export**: Download filtered results as CSV for CRM integration

## Scoring System

The tool calculates a **Propensity-to-Buy Score (0-100)** using these weighted criteria:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Role Fit** | 30 points | Job title relevance (Director of Toxicology, Head of Safety, etc.) |
| **Company Intent** | 20 points | Recent funding rounds (Series A/B/C, IPO) |
| **Technographic** | 15 points | Existing use of similar technology (3D models, organ-on-chip) |
| **Location** | 10 points | Proximity to biotech hubs (Boston, Bay Area, Basel, UK) |
| **Scientific Intent** | 40 points | Recent publications on DILI, liver toxicity, 3D models |

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or download this repository**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment variables** (optional):
```bash
cp .env.example .env
# Edit .env with your API keys if using external services
```

4. **Set up PubMed email** (required for PubMed API):
   - Edit `config/config.yaml`
   - Update the `pubmed.email` field with your email address

## Usage

### Running the Dashboard

```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Dashboard Features

1. **Search & Filter**:
   - Use the sidebar to filter by score, location, company, or biotech hub
   - Search box for quick name/title/company lookup

2. **Lead Table**:
   - View all leads with scores, contact info, and location data
   - Click on any lead for detailed score breakdown

3. **Analytics**:
   - Score distribution histograms
   - Top companies and location charts
   - Average scores by component

4. **Export**:
   - Click "Export CSV" to download filtered results

### Using Individual Components

#### Score a Single Lead

```python
from src.lead_scorer import LeadScorer

scorer = LeadScorer()

lead_data = {
    'title': 'Director of Toxicology',
    'location': 'Cambridge, MA',
    'company_description': 'Biotech using 3D liver models',
    'funding_info': {'round': 'Series B', 'date': '2025-01-01'},
    'publications': [{'title': 'DILI research', 'date': '2025-01-01'}]
}

scores = scorer.calculate_total_score(lead_data)
print(f"Total Score: {scores['total']}/100")
```

#### Search PubMed

```python
from src.pubmed_scraper import PubMedScraper

scraper = PubMedScraper(email='your-email@example.com')
publications = scraper.scrape(
    keywords=['DILI', 'drug-induced liver injury'],
    months_back=24,
    max_results=50
)
```

#### Process and Export Leads

```python
from src.data_aggregator import DataAggregator
from src.sample_data import SAMPLE_LEADS

aggregator = DataAggregator()
df = aggregator.process_leads(SAMPLE_LEADS)
aggregator.export_to_csv(df, 'my_leads.csv')
```

## Project Structure

```
euprime_ai_project/
├── app.py                      # Main Streamlit dashboard
├── requirements.txt            # Python dependencies
├── config/
│   └── config.yaml            # Configuration settings
├── src/
│   ├── scraper_base.py        # Base scraper class
│   ├── pubmed_scraper.py      # PubMed API scraper
│   ├── lead_scorer.py         # Scoring algorithm
│   ├── location_parser.py     # Location intelligence
│   ├── email_finder.py        # Email generation
│   ├── data_aggregator.py     # Data processing pipeline
│   └── sample_data.py         # Sample lead data
└── data/                       # Output directory for exports
```

## Data Sources

The tool can collect data from:

- **PubMed**: Scientific publications (using official NCBI API)
- **LinkedIn**: Professional profiles (requires API access or scraping)
- **Crunchbase/PitchBook**: Funding and investment data
- **Conference Sites**: SOT, AACR, ISSX attendee lists
- **NIH RePORTER**: Grant database for academic researchers

> **Note**: This demo uses sample data. For production use, you'll need API keys for LinkedIn, Crunchbase, and email enrichment services.

## Configuration

Edit `config/config.yaml` to customize:

- Search keywords for job titles and scientific terms
- Scoring weights for each criterion
- Biotech hub locations
- Rate limiting settings
- PubMed search parameters

## Compliance & Best Practices

⚠️ **Important Considerations**:

- **Web Scraping**: Some sites (especially LinkedIn) have anti-scraping policies. Use official APIs when possible.
- **Data Privacy**: Ensure GDPR/CCPA compliance when storing personal data.
- **Rate Limiting**: Respect API rate limits to avoid being blocked.
- **Email Validation**: Generated emails are patterns-based; validate before use.

## Demo

This implementation includes:
- ✅ Complete scoring algorithm with all 5 criteria
- ✅ PubMed scraper using official API
- ✅ Interactive dashboard with search and filters
- ✅ 20 sample leads for demonstration
- ✅ Export functionality
- ✅ Analytics and visualizations

## Next Steps for Production

1. **API Integration**:
   - LinkedIn Sales Navigator API or Proxycurl
   - Crunchbase API for funding data
   - Hunter.io or Apollo.io for email enrichment

2. **Database**:
   - PostgreSQL or MongoDB for lead storage
   - Automated data refresh pipelines

3. **Advanced Features**:
   - Email validation and verification
   - CRM integration (Salesforce, HubSpot)
   - Automated outreach sequences
   - Lead scoring model training with historical data

## Contact

For questions, feedback, or demo requests:

**Email**: akash@euprime.org

---

*Built with Python, Streamlit, and AI-powered scoring algorithms*
