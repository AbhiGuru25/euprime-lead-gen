"""
EuPrime AI Lead Generation Dashboard
Modern, user-friendly interface for lead generation and scoring.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.data_aggregator import DataAggregator
from src.sample_data import SAMPLE_LEADS
import os

# Page configuration
st.set_page_config(
    page_title="EuPrime Lead Generation | AI-Powered Lead Scoring",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS for modern, premium look
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Header with Gradient */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    
    .sub-header {
        font-size: 1.3rem;
        color: #64748b;
        margin-bottom: 2rem;
        text-align: center;
        font-weight: 500;
    }
    
    /* Metric Cards with Gradient Backgrounds */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Score Badges with Modern Design */
    .score-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 2rem;
        font-weight: 600;
        font-size: 0.9rem;
        color: white;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .score-high { 
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    }
    .score-medium { 
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    }
    .score-low { 
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background-color: #f8fafc;
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        font-size: 1.1rem;
        padding: 1rem 2rem;
    }
    
    /* Card Container */
    .info-card {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    
    /* Data Table Styling */
    .dataframe {
        border-radius: 0.5rem;
        overflow: hidden;
    }
    
    /* Success Message */
    .success-message {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    /* Feature Highlight */
    .feature-box {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-left: 4px solid #0ea5e9;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_and_process_data():
    """Load and process lead data."""
    aggregator = DataAggregator()
    df = aggregator.process_leads(SAMPLE_LEADS)
    return df


def get_score_badge(score):
    """Generate HTML badge for score."""
    if score >= 80:
        badge_class = "score-high"
        label = "High"
    elif score >= 50:
        badge_class = "score-medium"
        label = "Medium"
    else:
        badge_class = "score-low"
        label = "Low"
    
    return f'<span class="score-badge {badge_class}">{score}</span>'


def main():
    """Main application function."""
    
    # Clean Professional Header
    st.markdown('<div class="main-header">EuPrime Lead Generation</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-Powered Lead Scoring for 3D In-Vitro Models</div>', unsafe_allow_html=True)
    
    # Feature Highlight Banner
    st.markdown("""
        <div class="feature-box">
            <strong>Smart Lead Prioritization</strong> • Find the most qualified prospects for your 3D in-vitro models 
            using AI-powered scoring across 5 key criteria
        </div>
    """, unsafe_allow_html=True)
    
    # Load data with progress
    with st.spinner("Loading lead intelligence..."):
        df = load_and_process_data()
    
    # Enhanced Sidebar with Better Organization
    with st.sidebar:
        st.markdown("### Filters & Search")
        st.markdown("---")
        
        # Quick Stats in Sidebar
        st.markdown("#### Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Leads", len(df), delta=None)
        with col2:
            high_quality = len(df[df['score_total'] >= 80])
            st.metric("High Quality", high_quality, delta=None)
        
        st.markdown("---")
        
        # Search box (moved to top for better UX)
        st.markdown("#### Search")
        search_query = st.text_input(
            "Search leads...",
            placeholder="Name, Title, or Company",
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Score filter with indicator
        st.markdown("#### Score Filter")
        min_score = st.slider(
            "Minimum Propensity Score",
            min_value=0,
            max_value=100,
            value=0,
            step=5,
            help="Filter leads by their propensity-to-buy score"
        )
        
        # Show score range indicator
        if min_score >= 80:
            st.success("High-value leads only")
        elif min_score >= 50:
            st.info("Medium to high-value leads")
        else:
            st.info("All leads")
        
        st.markdown("---")
        
        # Advanced Filters (collapsible)
        with st.expander("Advanced Filters", expanded=False):
            # Location filter
            all_locations = sorted(df['person_location'].dropna().unique().tolist())
            selected_locations = st.multiselect(
                "Location",
                options=all_locations,
                default=[],
                help="Filter by person's location"
            )
            
            # Company filter
            all_companies = sorted(df['company'].dropna().unique().tolist())
            selected_companies = st.multiselect(
                "Company",
                options=all_companies,
                default=[],
                help="Filter by company name"
            )
            
            # Biotech hub filter
            all_hubs = sorted(df['biotech_hub'].dropna().unique().tolist())
            selected_hubs = st.multiselect(
                "Biotech Hub",
                options=all_hubs,
                default=[],
                help="Filter by major biotech hubs"
            )
        
        st.markdown("---")
        
        # Reset filters button
        if st.button("Reset All Filters"):
            st.rerun()
    
    # Apply filters
    filtered_df = df[df['score_total'] >= min_score].copy()
    
    if selected_locations:
        filtered_df = filtered_df[filtered_df['person_location'].isin(selected_locations)]
    
    if selected_companies:
        filtered_df = filtered_df[filtered_df['company'].isin(selected_companies)]
    
    if selected_hubs:
        filtered_df = filtered_df[filtered_df['biotech_hub'].isin(selected_hubs)]
    
    if search_query:
        mask = (
            filtered_df['name'].str.contains(search_query, case=False, na=False) |
            filtered_df['title'].str.contains(search_query, case=False, na=False) |
            filtered_df['company'].str.contains(search_query, case=False, na=False)
        )
        filtered_df = filtered_df[mask]
    
    # Reset rank after filtering
    filtered_df['rank'] = range(1, len(filtered_df) + 1)
    
    # Enhanced Metrics with Gradient Cards
    st.markdown("### Lead Intelligence Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1.5rem; border-radius: 1rem; text-align: center; color: white;">
                <div style="font-size: 2rem; font-weight: 700; margin: 0.5rem 0;">{}</div>
                <div style="font-size: 0.9rem; opacity: 0.9;">Total Leads</div>
            </div>
        """.format(len(df)), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                        padding: 1.5rem; border-radius: 1rem; text-align: center; color: white;">
                <div style="font-size: 2rem; font-weight: 700; margin: 0.5rem 0;">{}</div>
                <div style="font-size: 0.9rem; opacity: 0.9;">Filtered Results</div>
            </div>
        """.format(len(filtered_df)), unsafe_allow_html=True)
    
    with col3:
        avg_score = filtered_df['score_total'].mean() if len(filtered_df) > 0 else 0
        st.markdown("""
            <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); 
                        padding: 1.5rem; border-radius: 1rem; text-align: center; color: white;">
                <div style="font-size: 2rem; font-weight: 700; margin: 0.5rem 0;">{:.1f}</div>
                <div style="font-size: 0.9rem; opacity: 0.9;">Average Score</div>
            </div>
        """.format(avg_score), unsafe_allow_html=True)
    
    with col4:
        high_quality = len(filtered_df[filtered_df['score_total'] >= 80])
        st.markdown("""
            <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); 
                        padding: 1.5rem; border-radius: 1rem; text-align: center; color: white;">
                <div style="font-size: 2rem; font-weight: 700; margin: 0.5rem 0;">{}</div>
                <div style="font-size: 0.9rem; opacity: 0.9;">High Quality (≥80)</div>
            </div>
        """.format(high_quality), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["Lead Table", "Analytics", "About"])
    
    with tab1:
        st.markdown("### Qualified Leads Dashboard")
        
        # Export button with better styling
        col1, col2, col3 = st.columns([5, 1, 1])
        with col2:
            if len(filtered_df) > 0:
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="Export CSV",
                    data=csv,
                    file_name="euprime_leads.csv",
                    mime="text/csv"
                )
        with col3:
            st.markdown(f"**{len(filtered_df)}** leads")
        
        # Display table
        if len(filtered_df) > 0:
            # Info message
            if len(filtered_df) != len(df):
                st.info(f"Showing {len(filtered_df)} of {len(df)} total leads based on your filters")
            
            # Prepare display dataframe
            display_df = filtered_df[[
                'rank', 'score_total', 'name', 'title', 'company',
                'person_location', 'company_hq', 'email', 'biotech_hub'
            ]].copy()
            
            display_df.columns = [
                'Rank', 'Score', 'Name', 'Title', 'Company',
                'Person Location', 'Company HQ', 'Email', 'Biotech Hub'
            ]
            
            # Display with formatting
            st.dataframe(
                display_df,
                use_container_width=True,
                height=500,
                column_config={
                    "Rank": st.column_config.NumberColumn(
                        "Rank",
                        help="Lead ranking based on score",
                        format="%d"
                    ),
                    "Score": st.column_config.ProgressColumn(
                        "Score",
                        help="Propensity to Buy Score (0-100)",
                        format="%d",
                        min_value=0,
                        max_value=100,
                    ),
                    "Email": st.column_config.TextColumn(
                        "Email",
                        help="Business email address"
                    )
                },
                hide_index=True
            )
            
            # Detailed view expander
            st.subheader("Detailed Lead Information")
            selected_lead = st.selectbox(
                "Select a lead to view details:",
                options=filtered_df['name'].tolist(),
                index=0
            )
            
            if selected_lead:
                lead_data = filtered_df[filtered_df['name'] == selected_lead].iloc[0]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### Lead Information")
                    st.write(f"**Name:** {lead_data['name']}")
                    st.write(f"**Title:** {lead_data['title']}")
                    st.write(f"**Company:** {lead_data['company']}")
                    st.write(f"**Location:** {lead_data['person_location']}")
                    st.write(f"**Company HQ:** {lead_data.get('company_hq', 'N/A')}")
                    st.write(f"**Email:** {lead_data['email']}")
                    st.write(f"**Biotech Hub:** {lead_data.get('biotech_hub', 'N/A')}")
                
                with col2:
                    st.markdown("### Score Breakdown")
                    
                    # Create score breakdown chart
                    score_data = {
                        'Category': ['Role Fit', 'Company Intent', 'Technographic', 'Location', 'Scientific Intent'],
                        'Score': [
                            lead_data['score_role_fit'],
                            lead_data['score_company_intent'],
                            lead_data['score_technographic'],
                            lead_data['score_location'],
                            lead_data['score_scientific_intent']
                        ],
                        'Max': [30, 20, 15, 10, 40]
                    }
                    
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        name='Score',
                        x=score_data['Category'],
                        y=score_data['Score'],
                        marker_color='#1f77b4'
                    ))
                    fig.add_trace(go.Bar(
                        name='Max Possible',
                        x=score_data['Category'],
                        y=score_data['Max'],
                        marker_color='#d3d3d3',
                        opacity=0.3
                    ))
                    
                    fig.update_layout(
                        barmode='overlay',
                        height=300,
                        margin=dict(l=0, r=0, t=30, b=0),
                        title="Score Components"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.metric("Total Score", f"{lead_data['score_total']}/100")
        
        else:
            st.info("No leads match your current filters. Try adjusting the filters.")
    
    with tab2:
        st.subheader("Lead Analytics")
        
        if len(filtered_df) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                # Score distribution
                fig = px.histogram(
                    filtered_df,
                    x='score_total',
                    nbins=20,
                    title="Score Distribution",
                    labels={'score_total': 'Propensity Score'},
                    color_discrete_sequence=['#1f77b4']
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Top companies
                top_companies = filtered_df['company'].value_counts().head(10)
                fig = px.bar(
                    x=top_companies.values,
                    y=top_companies.index,
                    orientation='h',
                    title="Top 10 Companies",
                    labels={'x': 'Number of Leads', 'y': 'Company'},
                    color_discrete_sequence=['#2ca02c']
                )
                st.plotly_chart(fig, use_container_width=True)
            
            col3, col4 = st.columns(2)
            
            with col3:
                # Location distribution
                location_counts = filtered_df['biotech_hub'].value_counts()
                fig = px.pie(
                    values=location_counts.values,
                    names=location_counts.index,
                    title="Leads by Biotech Hub"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col4:
                # Score components average
                avg_scores = {
                    'Role Fit': filtered_df['score_role_fit'].mean(),
                    'Company Intent': filtered_df['score_company_intent'].mean(),
                    'Technographic': filtered_df['score_technographic'].mean(),
                    'Location': filtered_df['score_location'].mean(),
                    'Scientific Intent': filtered_df['score_scientific_intent'].mean()
                }
                
                fig = px.bar(
                    x=list(avg_scores.keys()),
                    y=list(avg_scores.values()),
                    title="Average Score by Component",
                    labels={'x': 'Component', 'y': 'Average Score'},
                    color_discrete_sequence=['#ff7f0e']
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("About This Tool")
        
        st.markdown("""
        ### EuPrime AI Lead Generation Tool
        
        This tool helps identify and rank qualified leads for EuPrime's 3D in-vitro models business.
        
        #### How It Works
        
        The tool uses a **Propensity-to-Buy Scoring System** with five weighted criteria:
        
        1. **Role Fit (30 points)**: Job title relevance (Director of Toxicology, Head of Safety, etc.)
        2. **Company Intent (20 points)**: Recent funding rounds (Series A/B/C, IPO)
        3. **Technographic (15 points)**: Existing use of similar technology (3D models, organ-on-chip)
        4. **Location (10 points)**: Proximity to biotech hubs (Boston, Bay Area, Basel, UK)
        5. **Scientific Intent (40 points)**: Recent publications on DILI, liver toxicity, 3D models
        
        **Total Score**: 0-100 (higher = more likely to buy)
        
        #### Data Sources
        
        - **PubMed**: Scientific publications and researcher information
        - **LinkedIn**: Professional profiles and company data
        - **Funding Databases**: Crunchbase, PitchBook for investment data
        - **Conference Listings**: SOT, AACR, ISSX attendees
        - **Grant Databases**: NIH RePORTER for academic researchers
        
        #### Features
        
        - 🔍 **Search & Filter**: Find leads by name, title, company, location
        - 📊 **Score Breakdown**: See detailed scoring for each lead
        - 📥 **Export**: Download filtered results as CSV
        - 📈 **Analytics**: Visualize lead distribution and trends
        
        #### Contact
        
        For questions or demo requests, contact: **akash@euprime.org**
        
        ---
        
        *Built with Python, Streamlit, and AI-powered scoring algorithms*
        """)


if __name__ == "__main__":
    main()
