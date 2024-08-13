# hellen/utils.py

from urllib.parse import urlparse, urlunparse, urljoin

def normalize_url(url, base_url=None, ignore_scheme=True):
    if base_url:
        url = urljoin(base_url, url)
    parsed_url = urlparse(url)
    scheme = 'https' if ignore_scheme else parsed_url.scheme
    netloc = parsed_url.netloc.replace('www.', '')  # Remove www.
    path = parsed_url.path
    if not path.endswith('/'):
        path += '/'  # Ensure trailing slash
    normalized_url = urlunparse(parsed_url._replace(scheme=scheme, netloc=netloc, path=path, query='', fragment=''))
    return normalized_url

def remove_duplicates(input_list):
    seen = set()
    output_list = []
    for item in input_list:
        if item not in seen:
            seen.add(item)
            output_list.append(item)
    return output_list

def handle_relative_links(base_url, urls):
    absolute_urls = [urljoin(base_url, url) for url in urls]
    return absolute_urls

def is_internal_link(base_url, link):
    base_domain = urlparse(base_url).netloc
    link_domain = urlparse(link).netloc
    return base_domain == link_domain

def filter_links(links):
    """
    Filters out unwanted links such as .xml, .jpg, .png, and other media files.

    Parameters:
    links (list): A list of URLs.

    Returns:
    list: A filtered list of URLs.
    """
    unwanted_extensions = ('.xml', '.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx', '.xls', '.xlsx')
    return [link for link in links if not link.endswith(unwanted_extensions)]
