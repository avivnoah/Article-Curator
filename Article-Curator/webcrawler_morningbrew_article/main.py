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

WORKER_LIMIT = 3
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
                page.goto("https://www.morningbrew.com/" + url)
                # Make sure the page has loaded, otherwise try another browser
                page.wait_for_selector('article', timeout=TIMEOUT_LIMIT)
                break
            except:
                if i <= 2:
                    print(f"Attempt #{i} failed on url: {url}")
                continue
        if browser == None:
            return ["Error - Browser didn't arise."]
        paragraphs = page.query_selector_all('a:has(p)')
        paragraphs = page.locator("div.article-body-content p").all_inner_texts()
        paragraphs = " ".join(paragraphs)
        return [url, paragraphs]


def main():
    global ARTICLE_LINKS
    ARTICLE_LINKS = gather_website_links()[0:2]  # Assuming gather_website_links returns a list of URLs
    print(ARTICLE_LINKS)

    #think of using docker

    global WORKER_LIMIT
    #print(CHECK_LIMIT_WORKERS)
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
    print(article_map)
    exit()
    print(f'Seconds To fulfill the data extraction: {(end - start)/2}\n')

    print("Inserting data into mongodb:\n")
    mongodb_repository.start_mongodb()
    mongodb_repository.upload_articles_to_mongodb(article_map)
    print("finished.")




if __name__ == "__main__":
    main()

