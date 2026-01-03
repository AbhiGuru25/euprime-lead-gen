"""
Sample lead data for demonstration purposes.
This file generates realistic sample data to showcase the dashboard functionality.
"""

import pandas as pd
from datetime import datetime, timedelta
import random

# Sample data
SAMPLE_LEADS = [
    {
        'name': 'Dr. Sarah Chen',
        'title': 'Director of Toxicology',
        'company': 'Vertex Pharmaceuticals',
        'person_location': 'Boston, MA',
        'company_hq': 'Boston, MA',
        'email': 'sarah.chen@vrtx.com',
        'linkedin': 'https://linkedin.com/in/sarah-chen',
        'company_description': 'Leading biotech company focused on drug discovery using 3D in vitro models and organ-on-chip technology for preclinical safety assessment',
        'funding_round': 'Public',
        'funding_date': '2020-01-15',
        'publications': 2,
        'recent_dili_paper': True
    },
    {
        'name': 'Dr. Michael Rodriguez',
        'title': 'Head of Preclinical Safety',
        'company': 'Moderna Therapeutics',
        'person_location': 'Cambridge, MA',
        'company_hq': 'Cambridge, MA',
        'email': 'm.rodriguez@modernatx.com',
        'linkedin': 'https://linkedin.com/in/michael-rodriguez',
        'company_description': 'Biotechnology company developing mRNA therapeutics with advanced preclinical testing platforms including hepatic spheroid models',
        'funding_round': 'Public',
        'funding_date': '2018-12-01',
        'publications': 3,
        'recent_dili_paper': True
    },
    {
        'name': 'Dr. Emily Watson',
        'title': 'VP Preclinical Development',
        'company': 'Genentech',
        'person_location': 'South San Francisco, CA',
        'company_hq': 'South San Francisco, CA',
        'email': 'watson.e@gene.com',
        'linkedin': 'https://linkedin.com/in/emily-watson',
        'company_description': 'Pioneering biotechnology company using innovative 3D cell culture systems for drug safety evaluation',
        'funding_round': 'Series C',
        'funding_date': '2024-08-20',
        'publications': 1,
        'recent_dili_paper': True
    },
    {
        'name': 'Dr. James Park',
        'title': 'Director Safety Pharmacology',
        'company': 'Amgen',
        'person_location': 'Thousand Oaks, CA',
        'company_hq': 'Thousand Oaks, CA',
        'email': 'jpark@amgen.com',
        'linkedin': 'https://linkedin.com/in/james-park-phd',
        'company_description': 'Global biopharmaceutical company with expertise in toxicology and preclinical safety assessment',
        'funding_round': 'Public',
        'funding_date': '1983-06-01',
        'publications': 1,
        'recent_dili_paper': False
    },
    {
        'name': 'Dr. Lisa Thompson',
        'title': 'Head of Safety Assessment',
        'company': 'Novartis',
        'person_location': 'Basel, Switzerland',
        'company_hq': 'Basel, Switzerland',
        'email': 'lisa.thompson@novartis.com',
        'linkedin': 'https://linkedin.com/in/lisa-thompson',
        'company_description': 'Pharmaceutical company investing in organ-on-chip and microphysiological systems for drug discovery',
        'funding_round': 'Public',
        'funding_date': '1996-01-01',
        'publications': 2,
        'recent_dili_paper': True
    },
    {
        'name': 'Dr. Robert Kim',
        'title': 'Senior Toxicologist',
        'company': 'Relay Therapeutics',
        'person_location': 'Cambridge, MA',
        'company_hq': 'Cambridge, MA',
        'email': 'r.kim@relaytx.com',
        'linkedin': 'https://linkedin.com/in/robert-kim',
        'company_description': 'Precision medicine company using computational and experimental approaches including 3D hepatic models',
        'funding_round': 'Series B',
        'funding_date': '2025-03-15',
        'publications': 1,
        'recent_dili_paper': True
    },
    {
        'name': 'Dr. Amanda Foster',
        'title': 'Director of Toxicology',
        'company': 'Alnylam Pharmaceuticals',
        'person_location': 'Cambridge, MA',
        'company_hq': 'Cambridge, MA',
        'email': 'afoster@alnylam.com',
        'linkedin': 'https://linkedin.com/in/amanda-foster',
        'company_description': 'RNAi therapeutics company with advanced in vitro liver toxicity screening platforms',
        'funding_round': 'Public',
        'funding_date': '2014-01-01',
        'publications': 2,
        'recent_dili_paper': True
    },
    {
        'name': 'Dr. David Martinez',
        'title': 'Toxicology Lead',
        'company': 'Beam Therapeutics',
        'person_location': 'Cambridge, MA',
        'company_hq': 'Cambridge, MA',
        'email': 'd.martinez@beamtx.com',
        'linkedin': 'https://linkedin.com/in/david-martinez',
        'company_description': 'Base editing company developing novel therapies with comprehensive preclinical safety programs',
        'funding_round': 'Series B',
        'funding_date': '2025-06-01',
        'publications': 1,
        'recent_dili_paper': False
    },
    {
        'name': 'Dr. Jennifer Lee',
        'title': 'Head of Hepatic Safety',
        'company': 'Recursion Pharmaceuticals',
        'person_location': 'Salt Lake City, UT',
        'company_hq': 'Salt Lake City, UT',
        'email': 'j.lee@recursion.com',
        'linkedin': 'https://linkedin.com/in/jennifer-lee-phd',
        'company_description': 'AI-driven drug discovery company utilizing 3D cell culture and liver spheroid models',
        'funding_round': 'Series C',
        'funding_date': '2024-11-10',
        'publications': 3,
        'recent_dili_paper': True
    },
    {
        'name': 'Dr. Thomas Anderson',
        'title': 'VP Safety Assessment',
        'company': 'AstraZeneca',
        'person_location': 'Cambridge, UK',
        'company_hq': 'Cambridge, UK',
        'email': 't.anderson@astrazeneca.com',
        'linkedin': 'https://linkedin.com/in/thomas-anderson',
        'company_description': 'Global pharmaceutical company with expertise in liver toxicity assessment and 3D models',
        'funding_round': 'Public',
        'funding_date': '1999-01-01',
        'publications': 2,
        'recent_dili_paper': True
    },
    {
        'name': 'Dr. Maria Garcia',
        'title': 'Principal Scientist - Toxicology',
        'company': 'Denali Therapeutics',
        'person_location': 'South San Francisco, CA',
        'company_hq': 'South San Francisco, CA',
        'email': 'm.garcia@denalitherapeutics.com',
        'linkedin': 'https://linkedin.com/in/maria-garcia',
        'company_description': 'Neurodegenerative disease company with advanced preclinical safety platforms',
        'funding_round': 'Series B',
        'funding_date': '2025-01-20',
        'publications': 1,
        'recent_dili_paper': False
    },
    {
        'name': 'Dr. Kevin Zhang',
        'title': 'Manager, Safety Pharmacology',
        'company': 'Intellia Therapeutics',
        'person_location': 'Cambridge, MA',
        'company_hq': 'Cambridge, MA',
        'email': 'k.zhang@intelliatx.com',
        'linkedin': 'https://linkedin.com/in/kevin-zhang',
        'company_description': 'CRISPR therapeutics company using in vitro liver models for safety assessment',
        'funding_round': 'Series A',
        'funding_date': '2025-04-15',
        'publications': 1,
        'recent_dili_paper': True
    },
    {
        'name': 'Dr. Rachel Cohen',
        'title': 'Senior Director, Toxicology',
        'company': 'Biogen',
        'person_location': 'Cambridge, MA',
        'company_hq': 'Cambridge, MA',
        'email': 'rachel.cohen@biogen.com',
        'linkedin': 'https://linkedin.com/in/rachel-cohen',
        'company_description': 'Biotechnology company focused on neuroscience with comprehensive toxicology programs',
        'funding_round': 'Public',
        'funding_date': '1991-01-01',
        'publications': 2,
        'recent_dili_paper': False
    },
    {
        'name': 'Dr. Christopher Brown',
        'title': 'Research Scientist',
        'company': 'Small Biotech Startup',
        'person_location': 'Austin, TX',
        'company_hq': 'Austin, TX',
        'email': 'c.brown@smallbiotech.com',
        'linkedin': 'https://linkedin.com/in/chris-brown',
        'company_description': 'Early-stage biotech company working on novel therapeutics',
        'funding_round': 'Seed',
        'funding_date': '2025-09-01',
        'publications': 0,
        'recent_dili_paper': False
    },
    {
        'name': 'Dr. Nicole White',
        'title': 'Associate Scientist',
        'company': 'Academic Research Lab',
        'person_location': 'New York, NY',
        'company_hq': 'New York, NY',
        'email': 'n.white@university.edu',
        'linkedin': 'https://linkedin.com/in/nicole-white',
        'company_description': 'University research laboratory studying basic biology',
        'funding_round': None,
        'funding_date': None,
        'publications': 0,
        'recent_dili_paper': False
    },
    {
        'name': 'Dr. Daniel Wilson',
        'title': 'Director of Preclinical Safety',
        'company': 'Roche',
        'person_location': 'Basel, Switzerland',
        'company_hq': 'Basel, Switzerland',
        'email': 'd.wilson@roche.com',
        'linkedin': 'https://linkedin.com/in/daniel-wilson',
        'company_description': 'Global healthcare company with advanced 3D in vitro toxicology platforms and organ-on-chip systems',
        'funding_round': 'Public',
        'funding_date': '1996-01-01',
        'publications': 3,
        'recent_dili_paper': True
    },
    {
        'name': 'Dr. Sophia Patel',
        'title': 'Head of Liver Safety',
        'company': 'GSK',
        'person_location': 'Stevenage, UK',
        'company_hq': 'London, UK',
        'email': 's.patel@gsk.com',
        'linkedin': 'https://linkedin.com/in/sophia-patel',
        'company_description': 'Pharmaceutical company investing in microphysiological liver models for DILI prediction',
        'funding_round': 'Public',
        'funding_date': '2001-01-01',
        'publications': 2,
        'recent_dili_paper': True
    },
    {
        'name': 'Dr. Alex Turner',
        'title': 'Toxicology Manager',
        'company': 'Takeda',
        'person_location': 'Cambridge, MA',
        'company_hq': 'Tokyo, Japan',
        'email': 'alex.turner@takeda.com',
        'linkedin': 'https://linkedin.com/in/alex-turner',
        'company_description': 'Global pharmaceutical company with hepatic safety assessment programs',
        'funding_round': 'Public',
        'funding_date': '2000-01-01',
        'publications': 1,
        'recent_dili_paper': False
    },
    {
        'name': 'Dr. Olivia Harris',
        'title': 'Senior Toxicologist',
        'company': 'Editas Medicine',
        'person_location': 'Cambridge, MA',
        'company_hq': 'Cambridge, MA',
        'email': 'o.harris@editasmedicine.com',
        'linkedin': 'https://linkedin.com/in/olivia-harris',
        'company_description': 'Gene editing company using 3D hepatocyte models for preclinical evaluation',
        'funding_round': 'Series B',
        'funding_date': '2025-02-28',
        'publications': 1,
        'recent_dili_paper': True
    },
    {
        'name': 'Dr. Brian Clark',
        'title': 'Principal Investigator',
        'company': 'Blueprint Medicines',
        'person_location': 'Cambridge, MA',
        'company_hq': 'Cambridge, MA',
        'email': 'b.clark@blueprintmedicines.com',
        'linkedin': 'https://linkedin.com/in/brian-clark',
        'company_description': 'Precision therapy company with comprehensive liver toxicity screening programs',
        'funding_round': 'Series C',
        'funding_date': '2024-10-05',
        'publications': 2,
        'recent_dili_paper': True
    }
]


def generate_sample_data():
    """Generate sample lead data with scores."""
    return pd.DataFrame(SAMPLE_LEADS)


if __name__ == "__main__":
    df = generate_sample_data()
    print(f"Generated {len(df)} sample leads")
    print(df[['name', 'title', 'company', 'person_location']].head())
