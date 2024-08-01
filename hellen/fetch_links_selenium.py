# fetch_links_selenium_stealth.py
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth

def fetch_all_links_selenium(url, headless=True):
    # Set up the WebDriver (Chrome in this case)
    options = Options()
    if headless:
        options.add_argument('--headless')  # Run in headless mode (without opening a browser window)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # Add your proxy server here if needed
    # options.add_argument('--proxy-server=http://your-proxy-server:port')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Apply selenium-stealth to the browser
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    try:
        # Open the webpage
        driver.get(url)

        # Perform some random actions to appear more human-like
        time.sleep(random.uniform(1, 3))  # Random delay
        actions = ActionChains(driver)
        actions.move_by_offset(random.randint(0, 100), random.randint(0, 100)).perform()
        time.sleep(random.uniform(1, 3))  # Random delay

        # Scroll down to simulate human interaction and trigger lazy loading
        for _ in range(3):
            driver.execute_script("window.scrollBy(0, document.body.scrollHeight / 3);")
            time.sleep(random.uniform(1, 3))  # Random delay

        # Wait for the page to load completely
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))

        # Debug: Print the page title and URL
        print(f"Page title: {driver.title}")
        print(f"Current URL: {driver.current_url}")

        # Debug: Print the page source (first 500 characters)
        page_source = driver.page_source
        print(f"Page source (first 500 chars): {page_source[:500]}")

        # Find all anchor tags
        anchors = driver.find_elements(By.TAG_NAME, 'a')
        print(f"Found {len(anchors)} anchor tags")

        # Extract and return the href attributes
        links = []
        for anchor in anchors:
            href = anchor.get_attribute('href')
            if href:
                links.append(href)
                # Debug: Print each href found
                print(f"Found link: {href}")

        return links

    except Exception as e:
        print(f"Error fetching {url} using Selenium: {e}")
        return []

    #finally:
        # Close the WebDriver
    #    driver.quit()

# Example usage
if __name__ == "__main__":
    url = 'https://cpyoga.com'
    headless = False  # Change this to True to run headless
    #links = fetch_all_links_selenium(url, headless=headless)
    links = fetch_all_links_selenium(url, headless=headless)
    for link in links:
        print(f"Link: {link}")
