# hellen/main.py
from hellen.fetch_links_requests import fetch_all_links_requests
from hellen.functions import normalize_url, remove_duplicates, handle_relative_links
from virginia import check_page_availability

def fetch_all_links(base_url):
    # Ignore www, http(s), and / at the end
    normalized_base_url = normalize_url(url=base_url, base_url=None, ignore_scheme=True)
    # Check if the page is available
    page_available = check_page_availability(normalized_base_url)
    
    if page_available:
        # Fetch all links from the URL, as is
        page_links = fetch_all_links_requests(url=normalized_base_url)
    else:
        # Return error
        page_links = "ERROR: base url unavailable"
    
    return page_links

def handle_links(base_url, page_links):
    absolute_links = handle_relative_links(base_url=base_url, urls=page_links)
    normalized_urls = [normalize_url(url, base_url=None, ignore_scheme=True) for url in absolute_links]
    unduplicated_links = remove_duplicates(input_list=normalized_urls)

    clean_links_list = unduplicated_links
    return clean_links_list

# Example usage
if __name__ == "__main__":
    base_url = 'https://smileup.pt'
    page_links = fetch_all_links(base_url=base_url)
    links = handle_links(base_url=base_url, page_links=page_links)
    
    for link in links:
        print(link)