# hectot/web_crawler.py
from urllib.parse import urlparse, urlunparse, urljoin



def normalize_url(url, base_url=None, ignore_scheme=True):
    if base_url:
        url = urljoin(base_url, url)
    parsed_url = urlparse(url)
    scheme = 'https' if ignore_scheme else parsed_url.scheme
    netloc = parsed_url.netloc.replace('www.', '')  # Remove www.
    normalized_url = urlunparse(parsed_url._replace(scheme=scheme, netloc=netloc, query='', fragment=''))
    if normalized_url.endswith('/'):
        normalized_url = normalized_url[:-1]
    return normalized_url

def remove_duplicates(input_list):
    """
    Removes duplicate records from a list while preserving the original order.
    
    Args:
    input_list (list): The list from which to remove duplicates.

    Returns:
    list: A new list with duplicates removed.
    """
    seen = set()
    output_list = []
    for item in input_list:
        if item not in seen:
            seen.add(item)
            output_list.append(item)
    return output_list

def handle_relative_links(base_url, urls):
    """
    Adds the base URL to the beginning of relative links in the given list.

    Args:
    base_url (str): The base URL to be added.
    urls (list): The list of URLs to be processed.

    Returns:
    list: A new list with absolute URLs.
    """
    absolute_urls = [urljoin(base_url, url) for url in urls]
    return absolute_urls

def is_internal_link(base_url, link):
    """
    Determine if a given link is internal to the base URL.

    Parameters:
    base_url (str): The base URL.
    link (str): The link to check.

    Returns:
    bool: True if the link is internal, False otherwise.
    """
    base_domain = urlparse(base_url).netloc
    link_domain = urlparse(link).netloc
    return base_domain == link_domain
