# src/scraper/product_scraper.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import csv
import json
from crawler import crawl_site
from .utils import get_soup

HEADERS = {"User-Agent": "Mozilla/5.0"}

# Data folder
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)





def scrape_product(url, category="", subcategory=""):
    soup = get_soup(url)
    if not soup:
        return None

    title = soup.select_one("h1.title")
    price = soup.select_one(".price")
    description = soup.select_one("p.description")
    rating_tag = soup.select_one("div.ratings span")  # works for this site

    return {
        "category": category,
        "subcategory": subcategory,
        "url": url,
        "title": title.text.strip() if title else "",
        "price": price.text.strip() if price else "",
        "description": description.text.strip() if description else "",
        "rating": rating_tag.text.strip() if rating_tag else ""
    }


def scrape_all_products(product_urls):
    detailed_products = []
    for idx, p in enumerate(product_urls, 1):
        print(f"Scraping {idx}/{len(product_urls)}: {p['url']}")
        data = scrape_product(p["url"], p["category"], p["subcategory"])
        if data:
            detailed_products.append(data)
    print(f"Scraped {len(detailed_products)} products in detail.")
    return detailed_products


def save_to_csv(products, filename="products.csv"):
    path = os.path.join(DATA_DIR, filename)
    if not products:
        print("No products to save.")
        return
    keys = products[0].keys()
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(products)
    print(f"Saved {len(products)} products to {path}")


def save_to_json(products, filename="products.json"):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=4, ensure_ascii=False)
    print(f"Saved {len(products)} products to {path}")


if __name__ == "__main__":
    # Crawl all product URLs
    product_urls = crawl_site()
    # Scrape all products
    detailed = scrape_all_products(product_urls)
    # Save final CSV & JSON
    save_to_csv(detailed)
    save_to_json(detailed)