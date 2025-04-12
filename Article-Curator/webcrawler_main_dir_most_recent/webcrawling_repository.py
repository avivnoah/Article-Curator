import json
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import mongodb_repository
from multiprocessing import cpu_count

def gather_links_parallel(sites_to_crawl: set, scroll_range=50, total_links_target=700):
    """
    This function handles link gathering in its totality
    :param sites_to_crawl: a set of sites to crawl
    :param scroll_range: amount of scrolls per page at most
    :param total_links_target: amount of links total
    :return: a set of all the links extracted
    """
    print(f"crawling for {total_links_target} links.")
    with open("site_config.json", "r") as config_file:
        site_configs = json.load(config_file)

    site_target = total_links_target // len(sites_to_crawl)
    all_links = []

    def crawl_single_site(site):
        config = site_configs[site]
        local_links = set()

        print(f"\n🚀 Crawling: {site}")

        with sync_playwright() as p:
            browser = p.firefox.launch(headless=True if config["headless"] == "True" else False)
            page = browser.new_page()
            stealth_sync(page)
            page.goto(config["url"] + config["article_link_pattern"])
            page.wait_for_selector('a:has(article)', timeout=15000)

            #page.wait_for_load_state("domcontentloaded", timeout=15000)
            for _ in range(scroll_range):
                if "scroll_down" in config:
                    page.mouse.wheel(0, 3500)
                selectors = config["link_selectors"]

                for selector in selectors:
                    try:
                        links = page.query_selector_all(selector)
                        for link in links:
                            href = link.get_attribute("href")
                            #if href and config["article_link_pattern"] in href:
                            if href:
                                local_links.add((site, href))
                                if len(local_links) >= site_target:
                                    break
                    except:
                        continue

                try:
                    if "load_more_button" in config:
                        page.locator(config["load_more_button"]).click()
                except:
                    break

                if len(local_links) >= site_target:
                    break

            browser.close()
            print(f"✅ {len(local_links)} links from {site}")
            return local_links

    with ThreadPoolExecutor(max_workers=len(sites_to_crawl)) as executor:
        results = executor.map(crawl_single_site, sites_to_crawl)
        for site_links in results:
            all_links.extend(site_links)

    print(f"\n🌐 Total unique links gathered: {len(all_links)}")
    return all_links

# --------- ARTICLE EXTRACTION ---------

def get_article_paragraphs(page, selectors):
    """
    This function processes each page, extracting paragraphs of texts from articles.
    :param page:
    :param selectors:
    :return a merged string of all of the paragraphs.
    """
    for selector in selectors:
        try:
            page.wait_for_selector(selector, timeout=15000)
            paragraphs = page.locator(selector).all_inner_texts()
            if paragraphs:
                return " ".join(paragraphs)
        except:
            continue
    return []

def extract_article_data_wrapper(args):
    """
    This function handles data gathering from each link.
    :param args:
    :return:
    """
    site_name, url = args
    print(f"📝 Extracting: {url}")

    with open("site_config.json", "r") as config_file:
        site_configs = json.load(config_file)
    config = site_configs[site_name]
    selectors = config["article_selectors"]

    with sync_playwright() as p:
        try:
            browser = p.firefox.launch(headless=True if config["headless"] == "True" else False)
            page = browser.new_page()
            stealth_sync(page)
            page.goto(config["url"] + url)
            data = get_article_paragraphs(page, selectors)
            browser.close()
            return (config["url"] + url, data)
        except Exception as e:
            print(f"❌ Failed to extract {url}: {e}")
            return (config["url"] + url, [])

# --------- MAIN ---------

def web_crawling_main_method():
    """
    This is the main function, running it would run the webcrawler.
    Make sure your site_config.json is configured correctly.
    :return:
    """
    target_sites = {"morningbrew", "emergingtechbrew"}

    # Step 1: Crawl all sites in parallel
    gathered_links = gather_links_parallel(target_sites)

    # Step 2: Prepare input for extraction
    extraction_input = list(gathered_links)

    # Step 3: Extract article content in parallel
    print("\n🔍 Extracting article contents...")
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=min(cpu_count(), 4)) as executor:
        extracted = list(executor.map(extract_article_data_wrapper, extraction_input))
    end = time.perf_counter()

    print(f"⏱ Extraction completed in {(end - start):.2f} seconds")

    # Step 4: Filter and store results
    article_map = {url: data for (url, data) in extracted if data}
    print(f"\n✅ Extracted {len(article_map)} articles.")

    print("\n📥 Inserting into MongoDB...")
    mongodb_repository.start_mongodb()
    mongodb_repository.upload_articles_to_mongodb(article_map)
    print("✅ All done.")
