"""
Email finder utility to generate and validate business email addresses.
"""

from typing import List, Optional, Dict
import re
import requests
from src.scraper_base import BaseScraper


class EmailFinder:
    """Generate and validate business email addresses."""
    
    # Common email patterns
    PATTERNS = [
        "{first}.{last}@{domain}",
        "{first}{last}@{domain}",
        "{first_initial}{last}@{domain}",
        "{first}_{last}@{domain}",
        "{last}.{first}@{domain}",
        "{first_initial}.{last}@{domain}"
    ]
    
    def __init__(self):
        """Initialize email finder."""
        pass
    
    def normalize_name(self, name: str) -> Dict[str, str]:
        """
        Normalize a person's name for email generation.
        
        Args:
            name: Full name string
            
        Returns:
            Dictionary with normalized name components
        """
        # Remove titles and suffixes
        name = re.sub(r'\b(Dr|Prof|Mr|Mrs|Ms|PhD|MD|Jr|Sr|III|II)\b\.?', '', name, flags=re.IGNORECASE)
        
        # Clean and split
        parts = name.strip().split()
        
        if len(parts) == 0:
            return {'first': '', 'last': '', 'first_initial': ''}
        elif len(parts) == 1:
            return {
                'first': parts[0].lower(),
                'last': '',
                'first_initial': parts[0][0].lower() if parts[0] else ''
            }
        else:
            first = parts[0].lower()
            last = parts[-1].lower()
            return {
                'first': first,
                'last': last,
                'first_initial': first[0] if first else ''
            }
    
    def extract_domain_from_company(self, company_name: str) -> str:
        """
        Extract likely email domain from company name.
        
        Args:
            company_name: Company name
            
        Returns:
            Likely email domain
        """
        # Remove common suffixes
        domain = company_name.lower()
        domain = re.sub(r'\s+(inc|llc|ltd|corp|corporation|company|co)\b\.?', '', domain, flags=re.IGNORECASE)
        
        # Remove special characters and spaces
        domain = re.sub(r'[^a-z0-9]', '', domain)
        
        # Add .com (most common)
        return f"{domain}.com"
    
    def generate_email_variations(self, name: str, company: str, custom_domain: Optional[str] = None) -> List[str]:
        """
        Generate possible email address variations.
        
        Args:
            name: Person's full name
            company: Company name
            custom_domain: Optional custom domain (e.g., 'pfizer.com')
            
        Returns:
            List of possible email addresses
        """
        name_parts = self.normalize_name(name)
        domain = custom_domain if custom_domain else self.extract_domain_from_company(company)
        
        emails = []
        for pattern in self.PATTERNS:
            try:
                email = pattern.format(
                    first=name_parts['first'],
                    last=name_parts['last'],
                    first_initial=name_parts['first_initial'],
                    domain=domain
                )
                # Only add if it has both parts (first and last name)
                if '@' in email and not email.startswith('@') and not '.@' in email:
                    emails.append(email)
            except KeyError:
                continue
        
        return emails
    
    def validate_email_format(self, email: str) -> bool:
        """
        Validate email format using regex.
        
        Args:
            email: Email address to validate
            
        Returns:
            True if valid format, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def find_most_likely_email(self, name: str, company: str, custom_domain: Optional[str] = None) -> str:
        """
        Find the most likely email address.
        
        Args:
            name: Person's full name
            company: Company name
            custom_domain: Optional custom domain
            
        Returns:
            Most likely email address
        """
        emails = self.generate_email_variations(name, company, custom_domain)
        
        if not emails:
            return ""
        
        # Return the most common pattern: first.last@domain
        return emails[0] if emails else ""


# Example usage
if __name__ == "__main__":
    finder = EmailFinder()
    
    # Test cases
    test_cases = [
        ("Dr. Jane Smith", "Pfizer Inc", "pfizer.com"),
        ("John Doe", "BioTech Corp", None),
        ("Sarah Johnson PhD", "Novartis", "novartis.com")
    ]
    
    for name, company, domain in test_cases:
        print(f"\nName: {name}")
        print(f"Company: {company}")
        print(f"Domain: {domain if domain else 'auto-generated'}")
        
        emails = finder.generate_email_variations(name, company, domain)
        print(f"Email variations:")
        for email in emails:
            print(f"  - {email}")
        
        most_likely = finder.find_most_likely_email(name, company, domain)
        print(f"Most likely: {most_likely}")
