import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.core.utils import read_version_from_cmd
from webdriver_manager.chrome import ChromeDriverManager
import requests

BASE_URL = "https://indiankanoon.org"

def get_chrome_version():
    """Get the installed Chrome version using system command."""
    try:
        return read_version_from_cmd("google-chrome", "--version")
    except Exception:
        return read_version_from_cmd("chrome", "--version")

def get_soup_with_selenium(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # ✅ Automatically match Chrome version
    driver_path = ChromeDriverManager().install()
    driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)

    driver.get(url)
    time.sleep(3)
    html = driver.page_source
    driver.quit()
    return BeautifulSoup(html, "html.parser")


def get_year_links():
    print(f"Fetching: {BASE_URL}/browse/union-act/")
    soup = get_soup_with_selenium(BASE_URL + "/browse/union-act/")
    year_links = soup.select("a[href*='/browse/union-act/']")
    years = []

    for link in year_links:
        href = link.get("href")
        if href and "/browse/union-act/" in href and href.count("/") == 3:
            years.append(BASE_URL + href)

    print(f"Found {len(years)} years.")
    return years


def get_acts_from_year(year_url):
    print(f"Fetching acts from {year_url}")
    soup = get_soup_with_selenium(year_url)
    acts = []
    for link in soup.select("a[href*='/doc/']"):
        title = link.text.strip()
        href = link.get("href")
        if title and href:
            acts.append({
                "title": title,
                "url": BASE_URL + href
            })
    return acts


def scrape_union_acts():
    all_data = []
    years = get_year_links()

    for year_link in years:
        acts = get_acts_from_year(year_link)
        all_data.extend(acts)
        print(f"→ {len(acts)} acts added from {year_link}")

    return all_data


if __name__ == "__main__":
    data = scrape_union_acts()
    print(f"\nTotal laws scraped: {len(data)}")

    with open("union_acts.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("✅ Data saved to union_acts.json")
