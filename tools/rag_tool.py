import requests
from bs4 import BeautifulSoup

class UniversityWebTool:
    def __init__(self):
        self.base_url = "https://uosahiwal.edu.pk"

    def search_university_data(self, query: str) -> str:
        """
        University ki website se relevant data scrape karne ka function.
        """
        try:
            # Note: Real-world mein hum specific sub-pages target karte hain jese admissions, fee etc.
            # Demo ke liye hum main page ya relevant links ko scrape kar rahe hain.
            response = requests.get(self.base_url, timeout=10)
            if response.status_code != 200:
                return "University website is currently unreachable."
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Website ka text data extract karna
            text_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'li'])
            all_text = [elem.get_text(strip=True) for elem in text_elements]
            
            # Query se match hone wale paragraphs filter karna
            relevant_chunks = [text for text in all_text if any(word in text.lower() for word in query.lower().split())]
            
            context = "\n".join(relevant_chunks[:5]) # Top 5 relevant matches return karna
            
            if not context:
                return "University of Sahiwal: Higher education institution in Sahiwal, Punjab, Pakistan. Offers admissions in CS, Business, and English. Specific query details not found on the main page scrape."
                
            return context
        except Exception as e:
            return f"Error fetching data from University website: {str(e)}"