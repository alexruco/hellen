# hectot/web_crawler.py

from functions import parse_sitemap, normalize_url, is_internal_url, is_content_page, is_non_page_link
from virginia import check_page_availability
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import time

def parse_html(page_content):
    """
    Parse the HTML content and extract all links.

    Parameters:
    page_content (str): The HTML content of the page.

    Returns:
    list: A list of extracted links.
    """
    soup = BeautifulSoup(page_content, 'html.parser')
    links = [a.get('href') for a in soup.find_all('a', href=True)]
    return links

def fetch_page_with_requests(url):
    """
    Fetch the page content using requests.

    Parameters:
    url (str): The URL of the page to fetch.

    Returns:
    str: The HTML content of the page, or None if fetching fails.
    """
    try:
        response = requests.get(url)
        if response.status_code == 403:
            return None
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {url} with requests: {str(e)}")
        return None

def fetch_page_with_selenium(driver, url):
    """
    Fetch the page content using Selenium.

    Parameters:
    driver (webdriver): The Selenium WebDriver instance.
    url (str): The URL of the page to fetch.

    Returns:
    str: The HTML content of the page, or None if fetching fails.
    """
    try:
        driver.get(url)
        time.sleep(2)  # Wait for the page to load
        return driver.page_source
    except Exception as e:
        print(f"Failed to fetch {url} with Selenium: {str(e)}")
        return None

def crawl_website(root_url, crawl_depth=5, is_sitemap=False):
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

    # Setup Selenium
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def crawl(url, current_depth):
        if current_depth > crawl_depth or url in visited_urls:
            return
        visited_urls.add(url)

        if is_sitemap:
            links = parse_sitemap(url)
        else:
            page_content = fetch_page_with_requests(url)
            if page_content is None:
                page_content = fetch_page_with_selenium(driver, url)
            if not page_content:
                return
            links = parse_html(page_content)

        for link in links:
            link_url = normalize_url(link, base_url=url, ignore_scheme=False)
            if is_internal_url(root_url, link_url) and is_content_page(link_url):
                status = check_page_availability(link_url)
                if link_url not in internal_links_data:
                    internal_links_data[link_url] = {
                        'link': link_url,
                        'available': status,
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
                        'available': status,
                        'found_at': []
                    }
                external_links_data[link_url]['found_at'].append(url)

        if is_sitemap:
            for link in links:
                if link.endswith('.xml'):
                    crawl(link, current_depth + 1)
                else:
                    status = check_page_availability(link)
                    sitemap_links_data.append({
                        'link': link,
                        'available': status,
                        'found_at': [url]
                    })

    crawl(root_url, 0)
    driver.quit()
    return list(internal_links_data.values()), list(external_links_data.values()), sitemap_links_data

# Example usage
if __name__ == "__main__":
    internal_links, external_links, sitemap_links = crawl_website("https://cpyoga.com/", 1, False)
    print(internal_links, external_links, sitemap_links)
