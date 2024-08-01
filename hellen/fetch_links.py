from fetch_links_requests import fetch_all_links_requests
from fetch_links_selenium import fetch_all_links_selenium
from functions import normalize_url
from virginia import check_page_availability

def fetch_all_links(baseurl):
      
    #ignore www, http(s) and / at the end
    url = normalize_url(baseurl)
    #check if the page is availbale
    page_available = check_page_availability(url)
    
    if(page_available):
        
        #more efficient, request is the default method 
        page_links = fetch_all_links_requests(url)
    else:
        #more effective, selenium is a call back
        page_links = fetch_all_links_selenium(url)
    
    return page_links

# Example usage
if __name__ == "__main__":
    url = 'https://cpyoga.com'
    links = fetch_all_links(url)
    for link in links:
        print(link)

