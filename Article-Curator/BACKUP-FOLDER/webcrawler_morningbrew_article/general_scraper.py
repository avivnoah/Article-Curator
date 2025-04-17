import sys

from playwright.sync_api import sync_playwright
from morningbrew_article_links_gatherer import gather_website_links, HEADLESS_VALUE, TIMEOUT_LIMIT
import concurrent
from playwright_stealth import stealth_sync
from multiprocessing import cpu_count
import time
from pymongo import MongoClient
import mongodb_repository
#Threads for IO Bound, Processes  for CPU bound
#Can change ProcessPoolExecutor() to ThreadPoolExecutor() and the program will run the same, but utilize threads!

#IDEAS:
#Instead of limiting worker count,
#think of utilizing a mechanism in which, if i get an error, i return the url, create a error list and rerun it/smth
#If I really want to speed the link processing even more, I can think of using multithreading within each process.

# WITH Following the site's robots.txt permissions.

# Constants
WEBSITE_URL = "https://www.morningbrew.com/search"
# The scrolls we want to execute on this current run -> The amount of links we'll gather * 12(based on current
# Morningbrew format)
SCROLL_RANGE = 3
HEADLESS_VALUE = True
TIMEOUT_LIMIT = 15000
CHECK_LIMIT_WORKERS = True

def extract_article_data(url):
    print("Extracting data from: " + url)
    with sync_playwright() as p:
        browser = None
        # Raise a working browser
        for i in range(4):
            try:
                if i==0:
                    browser = p.firefox.launch(executable_path="C:/Users/avivo/AppData/Local/ms-playwright/firefox-1447/firefox/firefox.exe", headless=HEADLESS_VALUE)
                #elif i==1:
                    #browser = p.chromium.launch(executable_path="C:/Users/avivo/AppData/Local/ms-playwright/chromium-1112/chrome-win/chrome.exe", headless=HEADLESS_VALUE)
                #elif i==2:
                    #browser = p.webkit.launch(executable_path="C:/Users/avivo/AppData/Local/ms-playwright/webkit-1992/playwright.exe", headless=HEADLESS_VALUE)
                else:
                    exit("Can't load the website... Darn Anti-Bot verification process!")
                # Set up a new broswer page
                page = browser.new_page()
                # Human-Verification bypass
                stealth_sync(page)
                # parse the new page url
                page.goto(url)
                # Make sure the page has loaded, otherwise try another browser
                page.wait_for_selector('div.kQHUvl', timeout=TIMEOUT_LIMIT)
                break
            except:
                if i <= 2:
                    print(f"Attempt #{i} failed on url: {url}")
                continue
        if browser == None:
            return ["Error - Browser didn't arise."]
        paragraphs = page.query_selector_all('div.kQHUvl p')
        data = []
        for paragraph in paragraphs:
            paragraph_text = paragraph.evaluate('(element) => element.textContent')
            data.append(paragraph_text)
        return [url, data[1:]]


def main():
    global ARTICLE_LINKS
    ARTICLE_LINKS = gather_website_links()  # Assuming gather_website_links returns a list of URLs
    #think of using docker

    global WORKER_LIMIT

    if not CHECK_LIMIT_WORKERS:
        WORKER_LIMIT = cpu_count()

    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor(max_workers=min(WORKER_LIMIT,cpu_count())) as executor:
        article_data = executor.map(extract_article_data, ARTICLE_LINKS)
    end = time.perf_counter()

    print("Extracted data:\n")
    article_map = {}
    for article in article_data:
        article_url, article_data = article[0], article[1]
        if article_data and article_data[0]:
            article_map[article_url] = article_data
        else:
            print(article_url)

    print(f'Seconds To fulfill the data extraction: {(end - start)/2}\n')

    print("Inserting data into mongodb:\n")
    mongodb_repository.start_mongodb()
    mongodb_repository.upload_articles_to_mongodb(article_map)


def gather_website_links():
    print(f'Link amount to be extracted: {(SCROLL_RANGE-1) * 12}')
    with sync_playwright() as p:
        browser = None
        # Raise a working browser
        for i in range(1):
            try:
                browser = p.firefox.launch(executable_path="C:/Users/avivo/AppData/Local/ms-playwright/firefox-1447/firefox/firefox.exe", headless=HEADLESS_VALUE)
                # Set up a new broswer page
                page = browser.new_page()
                # Human-Verification bypass
                stealth_sync(page)
                # parse the new page url
                page.goto(WEBSITE_URL)
                time.sleep(10)
                # Make sure the page has loaded, otherwise try another browser
                page.wait_for_load_state("domcontentloaded", timeout=TIMEOUT_LIMIT)
                #page.wait_for_selector('div.cfgXFN', timeout=TIMEOUT_LIMIT)
            except:
                return "Error - Browser didn't arise."

        if browser == None:
            return "Error - Browser didn't arise."


        # A set of all the links gathered
        links_list = set()
        print("Starting to gather links...")
        for x in range(SCROLL_RANGE):

            # Scroll down
            page.mouse.wheel(0, 3500)
            page.mouse.wheel(0, 3500)

            # The div in which all of the article links in Morningbrew sit in
            links = page.query_selector_all('a')

            # Process the links
            for link in links:
                href = link.get_attribute('href')
                links_list.add(href)

            # Find the 'Load More' button, until we scrolled to the limit of the page, or the scroll range we set
            try:
                button = page.locator('button:has-text("Load More")')
                #button = page.locator('//button[contains(concat( " ", @class, " " ), concat( " ", "css-1gm9mkh", " " ))]')
            except:
                break
            # Click the button
            button.click()

        # Output the article links we've gathered

        # LIFT A WORKER READING THREAD HERE
        # TAKE A CHUNK OF LINKS, APPEND IT TO A READING AGENT



        browser.close()
        p.stop()
        print(f"Finished gathering {len(links_list)} links.")
        return list(links_list)

if __name__ == "__main__":
    main()

