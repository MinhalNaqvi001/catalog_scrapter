# src/scraper/utils.py
#Purpose: Helper functions like safe requests, URL joining, text cleaning, price cleaning, deduplication.
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_soup(url, timeout=10):
   
    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"Failed to get {url}: {e}")
        return None

def clean_price(price_str):
    
    return float(price_str.replace("$", "").replace(",", ""))

def join_url(base, href):
    
    return urljoin(base, href)