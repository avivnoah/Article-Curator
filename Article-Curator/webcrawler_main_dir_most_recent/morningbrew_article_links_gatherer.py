#pip install pytest-playwright
from playwright.sync_api import sync_playwright
#pip install playwright-stealth
from playwright_stealth import stealth_sync
from sys import exit
import time


# WITH Following the site's robots.txt permissions.

# Constants
WEBSITE_URL = "https://www.morningbrew.com"
# The scrolls we want to execute on this current run -> The amount of links we'll gather * 12(based on current
# Morningbrew format)
SCROLL_RANGE = 3
HEADLESS_VALUE = False
TIMEOUT_LIMIT = 15000

def gather_website_links():
    print(f'Link amount to be extracted: {(SCROLL_RANGE-1) * 12}')
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
                page.goto(WEBSITE_URL + '/search')
                time.sleep(10)
                # Make sure the page has loaded, otherwise try another browser
                page.wait_for_selector('a:has(article)', timeout=TIMEOUT_LIMIT)
                break
            except:
                continue

        if browser == None:
            return "Error - Browser didn't arise."

        #page.wait_for_load_state('domcontentloaded', timeout=40000)
        #page.wait_for_selector('div.cqKibH a')
        #allow_load_time()

        # A set of all the links gathered
        links_list = set()
        print("Starting to gather links...")
        for x in range(SCROLL_RANGE):

            # Scroll down
            page.mouse.wheel(0, 3500)
            page.mouse.wheel(0, 3500)

            #print("scroll iteration: ", x + 1)

            # The div in which all of the article links in Morningbrew sit in
            print(page.query_selector_all("a href:has(article)"))
            links = page.query_selector_all('div.cfgXFN a')
            links = page.query_selector_all("a:has(article)")
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