'''
import requests
from bs4 import BeautifulSoup
import re
from virginia import check_page_availability

def log_error(error):
    print(error)

def extract_urls(text):
    """Extract all URLs from the given text."""
    return re.findall(r'https?://\S+', text)

def scrape_webpage(url):
    """Scrape the text content of a webpage."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
    except requests.RequestException as e:
        log_error(f"Failed to fetch {url}: {e}")
        return ""

def encode_urls(text):
    """Encode URLs in the text by replacing 'https://' with 'https_//'."""
    return text.replace('https://', 'https_//')



def is_internal_url(base_url, url):
    base_domain = urlparse(base_url).netloc
    target_domain = urlparse(url).netloc
    return base_domain == target_domain

def is_content_page(url):
    content_extensions = (
        '.php', '.pdf', '.html', '.htm', '.asp', '.aspx', '.jsp', '.jspx',
        '.cgi', '.pl', '.cfm', '.xml', '.json', '.md', '.txt'
    )
    media_extensions = (
        '.jpg', '.jpeg', '.gif', '.webp', '.png', '.bmp', '.svg', '.ico',
        '.tif', '.tiff', '.mp4', '.mkv', '.webm', '.mp3', '.wav', '.ogg',
        '.avi', '.mov', '.wmv', '.flv', '.swf', '.m4a', '.m4v', '.aac',
        '.3gp', '.3g2', '.midi', '.mid', '.wma', '.aac', '.ra', '.ram', 
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.odt', 
        '.ods', '.odp'
    )
    if any(url.lower().endswith(ext) for ext in content_extensions):
        return True
    if any(url.lower().endswith(ext) for ext in media_extensions):
        return False
    return True

def parse_html(url):
    """
    Parse an HTML page to extract links.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return [link['href'] for link in soup.find_all('a', href=True) if not is_non_page_link(link['href'])]
    except requests.RequestException as e:
        log_error(f"Failed to fetch {url}: {e}")
        return []


def parse_sitemap(url):
    """
    Parse an XML sitemap to extract links.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'xml')
        return [loc.text for loc in soup.find_all('loc') if not is_non_page_link(loc.text)]
    except requests.RequestException as e:
        log_error(f"Failed to fetch {url}: {e}")
        return []


def is_non_page_link(link):
    """
    Determine if a link is a non-page link such as phone numbers, emails, or other protocols.
    """
    non_page_protocols = ('tel:', 'mailto:', 'whatsapp:', 'javascript:')
    return any(link.startswith(protocol) for protocol in non_page_protocols)



    """
    Recursively crawl a website starting from the root URL up to the specified depth.
    Collects internal links and external links, their status, and the URLs where they are found.
    
    Parameters:
    root_url (str): The root URL to start crawling from.
    crawl_depth (int): The depth to which the crawler should go. Default is 5.
    is_sitemap (bool): Indicates whether the root URL is a sitemap.
    
    Returns:
    tuple: Three lists of dictionaries containing the internal, external, and sitemap links, their status, and the URLs where they are found.
    """

    internal_links_data = {}
    external_links_data = {}
    sitemap_links_data = []

    visited_urls = set()

    def crawl(url, current_depth):
        if current_depth > crawl_depth or url in visited_urls:
            return
        visited_urls.add(url)

        if is_sitemap:
            links = parse_sitemap(url)
        else:
            links = parse_html(url)

        for link in links:
            link_url = normalize_url(link, base_url=url, ignore_scheme=False)
            if is_internal_url(root_url, link_url) and is_content_page(link_url):
                status = check_page_availability(link_url)
                if link_url not in internal_links_data:
                    internal_links_data[link_url] = {
                        'link': link_url,
                        'status': status,
                        'found_at': []
                    }
                internal_links_data[link_url]['found_at'].append(url)
                if not is_sitemap:
                    crawl(link_url, current_depth + 1)
            elif not is_internal_url(root_url, link_url) and not is_sitemap:
                status = check_page_availability(link_url)
                if link_url not in external_links_data:
                    external_links_data[link_url] = {
                        'link': link_url,
                        'status': status,
                        'found_at': []
                    }
                external_links_data[link_url]['found_at'].append(url)

        if is_sitemap:
            for link in links:
                if link.endswith('.xml'):
                    crawl(link, current_depth + 1)
                else:
                    status = get_http_status(link)
                    sitemap_links_data.append({
                        'link': link,
                        'status': status,
                        'found_at': [url]
                    })

    crawl(root_url, 0)
    return list(internal_links_data.values()), list(external_links_data.values()), sitemap_links_data
    '''