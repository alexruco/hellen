# fetch_links_requests.py
import requests
from bs4 import BeautifulSoup

def fetch_all_links_requests(url):
    
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        # Send a GET request to the URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all anchor tags
        anchors = soup.find_all('a', href=True)

        # Extract and return the href attributes
        links = [anchor['href'] for anchor in anchors]
        return links

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

# Example usage
if __name__ == "__main__":
    url = 'https://mysitefaster.com'
    links = fetch_all_links_requests(url)
    for link in links:
        print(link)
