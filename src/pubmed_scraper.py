"""
PubMed scraper to find researchers who have published relevant papers
on DILI, 3D models, liver toxicity, etc.
"""

from typing import List, Dict, Optional
from Bio import Entrez
from datetime import datetime, timedelta
import time
from src.scraper_base import BaseScraper


class PubMedScraper(BaseScraper):
    """Scraper for PubMed scientific publications."""
    
    def __init__(self, email: str, delay: float = 0.5):
        """
        Initialize PubMed scraper.
        
        Args:
            email: Email address (required by NCBI)
            delay: Delay between requests (NCBI recommends 0.33s minimum)
        """
        super().__init__(delay=delay)
        Entrez.email = email
        self.logger.info(f"PubMed scraper initialized with email: {email}")
    
    def build_search_query(self, keywords: List[str], months_back: int = 24) -> str:
        """
        Build a PubMed search query.
        
        Args:
            keywords: List of keywords to search for
            months_back: How many months back to search
            
        Returns:
            Search query string
        """
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months_back * 30)
        
        # Format dates for PubMed (YYYY/MM/DD)
        date_range = f"{start_date.strftime('%Y/%m/%d')}:{end_date.strftime('%Y/%m/%d')}[pdat]"
        
        # Combine keywords with OR
        keyword_query = " OR ".join([f'"{kw}"' for kw in keywords])
        
        # Full query
        query = f"({keyword_query}) AND {date_range}"
        
        return query
    
    def search_pubmed(self, query: str, max_results: int = 100) -> List[str]:
        """
        Search PubMed and return list of PMIDs.
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of PubMed IDs (PMIDs)
        """
        self._rate_limit()
        
        try:
            self.logger.info(f"Searching PubMed with query: {query}")
            handle = Entrez.esearch(
                db="pubmed",
                term=query,
                retmax=max_results,
                sort="relevance"
            )
            record = Entrez.read(handle)
            handle.close()
            
            pmids = record["IdList"]
            self.logger.info(f"Found {len(pmids)} publications")
            return pmids
            
        except Exception as e:
            self.logger.error(f"Error searching PubMed: {str(e)}")
            return []
    
    def fetch_publication_details(self, pmids: List[str]) -> List[Dict]:
        """
        Fetch detailed information for a list of PMIDs.
        
        Args:
            pmids: List of PubMed IDs
            
        Returns:
            List of publication dictionaries
        """
        if not pmids:
            return []
        
        publications = []
        
        # Fetch in batches of 10 to avoid overwhelming the API
        batch_size = 10
        for i in range(0, len(pmids), batch_size):
            batch = pmids[i:i + batch_size]
            self._rate_limit()
            
            try:
                self.logger.info(f"Fetching details for PMIDs {i+1}-{min(i+batch_size, len(pmids))}")
                handle = Entrez.efetch(
                    db="pubmed",
                    id=batch,
                    rettype="medline",
                    retmode="xml"
                )
                records = Entrez.read(handle)
                handle.close()
                
                for record in records['PubmedArticle']:
                    pub_data = self._parse_publication(record)
                    if pub_data:
                        publications.append(pub_data)
                        
            except Exception as e:
                self.logger.error(f"Error fetching publication details: {str(e)}")
                continue
        
        return publications
    
    def _parse_publication(self, record: Dict) -> Optional[Dict]:
        """
        Parse a PubMed record into a structured dictionary.
        
        Args:
            record: PubMed record from Entrez
            
        Returns:
            Dictionary with publication data
        """
        try:
            article = record['MedlineCitation']['Article']
            
            # Extract title
            title = article.get('ArticleTitle', '')
            
            # Extract abstract
            abstract = ''
            if 'Abstract' in article:
                abstract_texts = article['Abstract'].get('AbstractText', [])
                if isinstance(abstract_texts, list):
                    abstract = ' '.join(str(text) for text in abstract_texts)
                else:
                    abstract = str(abstract_texts)
            
            # Extract publication date
            pub_date = None
            if 'ArticleDate' in article and article['ArticleDate']:
                date_info = article['ArticleDate'][0]
                try:
                    year = int(date_info.get('Year', 0))
                    month = int(date_info.get('Month', 1))
                    day = int(date_info.get('Day', 1))
                    pub_date = datetime(year, month, day).isoformat()
                except:
                    pass
            
            # Extract authors
            authors = []
            if 'AuthorList' in article:
                for author in article['AuthorList']:
                    author_info = {
                        'last_name': author.get('LastName', ''),
                        'first_name': author.get('ForeName', ''),
                        'initials': author.get('Initials', ''),
                        'affiliation': author.get('AffiliationInfo', [{}])[0].get('Affiliation', '') if author.get('AffiliationInfo') else ''
                    }
                    authors.append(author_info)
            
            # Identify corresponding author (usually last author in biomedical research)
            corresponding_author = None
            first_author = None
            
            if authors:
                first_author = authors[0]
                corresponding_author = authors[-1]  # Typically the last author
            
            # Extract PMID
            pmid = record['MedlineCitation']['PMID']
            
            return {
                'pmid': str(pmid),
                'title': title,
                'abstract': abstract,
                'date': pub_date,
                'authors': authors,
                'first_author': first_author,
                'corresponding_author': corresponding_author,
                'url': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            }
            
        except Exception as e:
            self.logger.error(f"Error parsing publication: {str(e)}")
            return None
    
    def scrape(self, keywords: List[str], months_back: int = 24, max_results: int = 100) -> List[Dict]:
        """
        Main scraping method to search PubMed and fetch publication details.
        
        Args:
            keywords: List of keywords to search for
            months_back: How many months back to search
            max_results: Maximum number of results
            
        Returns:
            List of publication dictionaries with author information
        """
        # Build search query
        query = self.build_search_query(keywords, months_back)
        
        # Search PubMed
        pmids = self.search_pubmed(query, max_results)
        
        if not pmids:
            self.logger.warning("No publications found")
            return []
        
        # Fetch publication details
        publications = self.fetch_publication_details(pmids)
        
        self.logger.info(f"Successfully scraped {len(publications)} publications")
        return publications
    
    def extract_leads_from_publications(self, publications: List[Dict]) -> List[Dict]:
        """
        Extract potential leads from publication data.
        
        Args:
            publications: List of publication dictionaries
            
        Returns:
            List of lead dictionaries with researcher information
        """
        leads = []
        
        for pub in publications:
            # Extract corresponding author (budget holder)
            if pub.get('corresponding_author'):
                author = pub['corresponding_author']
                lead = {
                    'name': f"{author.get('first_name', '')} {author.get('last_name', '')}".strip(),
                    'title': 'Researcher',  # Will need to be enriched
                    'affiliation': author.get('affiliation', ''),
                    'source': 'PubMed',
                    'publications': [pub],
                    'pubmed_url': pub.get('url', '')
                }
                leads.append(lead)
        
        return leads


# Example usage
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    email = os.getenv('PUBMED_EMAIL', 'your-email@example.com')
    scraper = PubMedScraper(email=email)
    
    # Search for DILI-related publications
    keywords = [
        'DILI',
        'drug-induced liver injury',
        '3D hepatic model',
        'liver spheroid'
    ]
    
    publications = scraper.scrape(keywords, months_back=24, max_results=10)
    
    print(f"\nFound {len(publications)} publications")
    for i, pub in enumerate(publications[:3], 1):
        print(f"\n{i}. {pub['title']}")
        print(f"   Date: {pub['date']}")
        if pub['corresponding_author']:
            author = pub['corresponding_author']
            print(f"   Corresponding Author: {author['first_name']} {author['last_name']}")
            print(f"   Affiliation: {author.get('affiliation', 'N/A')[:100]}...")
    
    # Extract leads
    leads = scraper.extract_leads_from_publications(publications)
    print(f"\n\nExtracted {len(leads)} potential leads from publications")
