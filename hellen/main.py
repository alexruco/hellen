# hellen/main.py
from fetch_links_requests import fetch_all_links_requests
from utils import normalize_url, remove_duplicates, handle_relative_links, is_internal_link, filter_links
from virginia import check_page_availability

def internal_links_on_page(url):
    """
    Retrieve only the internal links from a given page.

    Parameters:
    url (str): The URL from which to retrieve the internal links.

    Returns:
    list: A list of internal links found on the page.
    """
    # Fetch all links on the page
    all_links = links_on_page(url)
    
    # Filter out only the internal links
    internal_links = [link for link in all_links if is_internal_link(url, link)]
    
    return internal_links

def external_links_on_page(url):
    """
    Retrieve only the external links from a given page.

    Parameters:
    url (str): The URL from which to retrieve the external links.

    Returns:
    list: A list of external links found on the page.
    """
    # Fetch all links on the page
    all_links = links_on_page(url)
    
    # Filter out only the external links
    external_links = [link for link in all_links if not is_internal_link(url, link)]
    
    return external_links

def links_on_page(url):
    """
    Retrieve and clean all links from a given page.

    Parameters:
    url (str): The URL from which to retrieve the links.

    Returns:
    list: A list of cleaned and filtered links found on the page.
    """
    page_links = fetch_all_links(url)
    
    # If fetch_all_links returns None or an empty list, return an empty list
    if not page_links:
        return []
    
    cleaned_links = handle_links(url, page_links)
    return cleaned_links

def fetch_all_links(url):
    """
    Fetch all the links from a given base URL.

    Parameters:
    base_url (str): The base URL from which to fetch the links.

    Returns:
    list: A list of links found on the page.
    """
    # Normalize the base URL
    normalized_base_url = normalize_url(url=url, base_url=None, ignore_scheme=True)
    
    # Assume the page is available for testing
    page_available = True

    if page_available:
        # Fetch all links from the URL
        page_links = fetch_all_links_requests(url=normalized_base_url)
        if not page_links:
            print(f"WARNING: No links found for {normalized_base_url}")
            return []
    else:
        print(f"ERROR: Base URL unavailable - {normalized_base_url}")
        return []
    
    return page_links

def handle_links(base_url, page_links):
    """
    Process and clean the list of links.

    Parameters:
    base_url (str): The base URL for normalization.
    page_links (list): The list of links to process.

    Returns:
    list: A cleaned and filtered list of links.
    """
    absolute_links = handle_relative_links(base_url=base_url, urls=page_links)
    normalized_urls = [normalize_url(url, base_url=None, ignore_scheme=True) for url in absolute_links]
    filtered_urls = filter_links(normalized_urls)
    unduplicated_links = remove_duplicates(input_list=filtered_urls)
    
    return unduplicated_links

# Example usage
if __name__ == "__main__":
    base_url = 'https://orca.ricarela.com/'
    page_links = external_links_on_page(url=base_url)
    
    if not page_links:
        print(f"No links to process for {base_url}")
    else:
        links = external_links_on_page(url=base_url)
        for link in links:
            print(link)
