# src/scraper/parsers.py
#Purpose: Scrape product details from each product page
from typing import List, Dict
from .utils import get_soup, clean_price

def scrape_product(url: str, category: str = "", subcategory: str = "") -> Dict:
    soup = get_soup(url)
    if not soup:
        return {}
    title_tag = soup.select_one("h1") or soup.select_one("a.title")
    price_tag = soup.select_one(".price")
    desc_tag = soup.select_one("p.description")
    rating_tag = soup.select_one("div.ratings span")
    
    return {
        "category": category,
        "subcategory": subcategory,
        "url": url,
        "title": title_tag.text.strip() if title_tag else "",
        "price": price_tag.text.strip() if price_tag else "",
        "description": desc_tag.text.strip() if desc_tag else "",
        "rating": rating_tag.text.strip() if rating_tag else ""
    }

def scrape_all_products(product_links: List[Dict]) -> List[Dict]:
    all_products = []
    for i, p in enumerate(product_links, 1):
        print(f"Scraping {i}/{len(product_links)}: {p['url']}")
        product = scrape_product(p["url"], p["category"], p["subcategory"])
        if product:
            all_products.append(product)
    return all_products