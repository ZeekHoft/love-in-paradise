import requests
from bs4 import BeautifulSoup

# URL of the Rappler homepage
url = 'https://www.rappler.com'

# Send a GET request to fetch the HTML content
response = requests.get(url)
response.raise_for_status()  # Raise an exception for HTTP errors

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all headline elements based on their HTML tags and classes
# This is an example; adjust the tag and class based on actual inspection
headline_elements = soup.find_all('h3', class_='story-title')

# Extract and print the text of each headline
headlines = [headline.get_text(strip=True) for headline in headline_elements]

for idx, headline in enumerate(headlines, start=1):
    print(f"{idx}. {headline}")
