# hellen/main.py
from hellen.fetch_links_requests import fetch_all_links_requests
from hellen.utils import normalize_url, remove_duplicates, handle_relative_links
from virginia import check_page_availability

def links_on_page(base_url):
    page_links = fetch_all_links(base_url)
    
    # If fetch_all_links returns None or an empty list, return an empty list
    if not page_links:
        return []
    
    cleaned_links = handle_links(base_url, page_links)
    return cleaned_links

def fetch_all_links(base_url):
    # Ignore www, http(s), and / at the end
    normalized_base_url = normalize_url(url=base_url, base_url=None, ignore_scheme=True)
    
    # Temporarily bypass check_page_availability for testing
    page_available = True  # Force it to assume the page is available

    if page_available:
        # Fetch all links from the URL, as is
        page_links = fetch_all_links_requests(url=normalized_base_url)
        if not page_links:
            # In case of failure, log or return an empty list
            print(f"WARNING: No links found for {normalized_base_url}")
            return []
    else:
        # Log the error and return an empty list
        print(f"ERROR: Base URL unavailable - {normalized_base_url}")
        return []
    
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
    
    # Handle the case where no links are returned
    if not page_links:
        print(f"No links to process for {base_url}")
    else:
        links = links_on_page(base_url=base_url)
        for link in links:
            print(link)
