# fetch_links_requests.py

import requests
from bs4 import BeautifulSoup

def fetch_all_links_requests(url, sitemap_crawl=False):
    """
    Fetches all links from the given URL. If sitemap_crawl is True, fetches only links ending with .xml.
    If sitemap_crawl is False, fetches all links except those ending with .xml.
    
    Args:
    url (str): The URL to fetch links from.
    sitemap_crawl (bool): If True, fetches only .xml links. Defaults to False.

    Returns:
    list: A list of links.
    """
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

        # Extract and filter the href attributes
        if sitemap_crawl:
            links = [anchor['href'] for anchor in anchors if anchor['href'].lower().endswith('.xml')]
        else:
            links = [anchor['href'] for anchor in anchors if not anchor['href'].lower().endswith('.xml')]

        return links

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

# Example usage
if __name__ == "__main__":
    url = 'https://mysitefaster.com'
    links = fetch_all_links_requests(url, sitemap_crawl=False)  # Fetch all links except XML links
    for link in links:
        print(link)
