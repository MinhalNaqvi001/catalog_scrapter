# src/scraper/crawler.py
from typing import List, Dict
from .utils import get_soup, join_url

BASE_URL = "https://webscraper.io/test-sites/e-commerce/static"

def find_categories() -> List[Dict[str, str]]:
    soup = get_soup(BASE_URL)
    if not soup:
        return []

    categories = []
    # Better selector — sidebar navigation links
    for link in soup.select('div.sidebar-nav a[href^="/test-sites/e-commerce/static/"]'):
        name = link.text.strip()
        href = link.get("href")
        if name and href and "allinone" not in href.lower():
            full_url = join_url(BASE_URL, href)
            categories.append({"name": name, "url": full_url})

    return categories


def find_subcategories(category_url: str) -> List[Dict[str, str]]:
    soup = get_soup(category_url)
    if not soup:
        return []

    subcats = []
    # Common pattern on this test site
    for link in soup.select('div.col-lg-3 div.card a[href^="/test-sites/e-commerce/static/"]'):
        name = link.text.strip()
        href = link.get("href")
        if name and href:
            full_url = join_url(category_url, href)
            if full_url != category_url:
                subcats.append({"name": name, "url": full_url})

    # Fallback if above doesn't work
    if not subcats:
        for link in soup.select('a[href*="/computers/"][href*="/"], a[href*="/phones/"]'):
            name = link.text.strip()
            href = link.get("href")
            if name and href and len(name) > 2:
                full_url = join_url(category_url, href)
                if full_url != category_url and "allinone" not in full_url:
                    subcats.append({"name": name, "url": full_url})

    return subcats


def get_all_product_links_from_listing(start_url: str, category: str = "", subcategory: str = "") -> List[Dict]:
    products = []
    current_url = start_url
    page = 1

    while current_url:
        print(f"  Page {page}: {current_url}")
        soup = get_soup(current_url)
        if not soup:
            break

        # FIXED: better product link collection
        for card in soup.select('div.thumbnail'):
            title_link = card.select_one('a.title')
            if title_link and title_link.get('href'):
                products.append({
                    "category": category,
                    "subcategory": subcategory,
                    "url": join_url(current_url, title_link['href'])
                })

        # FIXED: more reliable next-page detection
        next_btn = None
        # Best selector for this site
        next_btn = soup.select_one('a[aria-label="Next"]')
        if not next_btn:
            next_btn = soup.select_one('li.next a, li.page-item.next a')
        if not next_btn:
            next_btn = soup.find('a', string=lambda t: t and '›' in str(t).strip())

        if next_btn and next_btn.get('href'):
            current_url = join_url(current_url, next_btn['href'])
            page += 1
        else:
            current_url = None

    return products


def crawl_site() -> List[Dict]:
    all_products = []
    categories = find_categories()
    print(f"Found {len(categories)} categories")

    for cat in categories:
        print(f"→ {cat['name']}")
        subcats = find_subcategories(cat["url"])

        if not subcats:
            print("   (no subcategories found → crawling directly)")
            items = get_all_product_links_from_listing(cat["url"], cat["name"])
            all_products.extend(items)
        else:
            for sub in subcats:
                print(f"   → {sub['name']}")
                items = get_all_product_links_from_listing(sub["url"], cat["name"], sub["name"])
                all_products.extend(items)

    # Simple deduplication by URL (just in case)
    seen_urls = set()
    unique = []
    for p in all_products:
        if p["url"] not in seen_urls:
            seen_urls.add(p["url"])
            unique.append(p)

    print(f"Total unique product URLs found: {len(unique)}")
    return unique