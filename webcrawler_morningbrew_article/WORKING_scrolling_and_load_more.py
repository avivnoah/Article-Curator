from playwright.sync_api import sync_playwright
import pandas as pd
import time

def main():
    with sync_playwright() as p:
        browser = p.firefox.launch(executable_path="C:/Users/avivo/AppData/Local/ms-playwright/firefox-1447/firefox/firefox.exe", headless=False)
        page = browser.new_page()
        page.goto('https://www.morningbrew.com/search')
        time.sleep(15)
        page.wait_for_load_state('networkidle')
        # process scrolling down
        for x in range(100):
            page.mouse.wheel(0, 15000)
            page.mouse.wheel(0, 15000)
            print("scrolling", x)
            time.sleep(2)

            # Find the button using a CSS selector
            #button = page.locator('chakra-button css-gd19v')
            button = page.locator('button:has-text("Load More")')
            #button = page.locator('//button[contains(concat( " ", @class, " " ), concat( " ", "css-1gm9mkh", " " ))]')


            # Alternatively, you can use an XPath expression
            # button = page.locator('//button[@id="button-id"]')

            # Click the button
            button.click()
            time.sleep(2)

        browser.close()
        p.stop()

if __name__ == "__main__":
    main()