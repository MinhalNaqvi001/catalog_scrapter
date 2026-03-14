#Purpose: Orchestrates full workflow: crawl → scrape → export → analysis.
# src/main.py
from scraper.crawler import crawl_site
from scraper.parsers import scrape_all_products
from scraper.exporters import save_to_csv, save_to_json
import pandas as pd
import os

def main():
    # 1️⃣ Crawl all product URLs
    product_links = crawl_site()
    print(f"Total product URLs found: {len(product_links)}")

    # 2️⃣ Scrape product details
    all_products = scrape_all_products(product_links)
    print(f"Scraped {len(all_products)} products in detail.")

    # 3️⃣ Export
    DATA_FOLDER = os.path.join(os.path.dirname(__file__), "data")
    save_to_csv(all_products, folder=DATA_FOLDER)
    save_to_json(all_products, folder=DATA_FOLDER)

    # 4️⃣ Analysis (optional, can also be separate file)
    csv_path = os.path.join(DATA_FOLDER, "products.csv")
    df = pd.read_csv(csv_path)
    df["price_clean"] = df["price"].str.replace("$", "").str.replace(",", "").astype(float)

    print("\nProducts per category:")
    print(df["category"].value_counts())

    print("\nProducts per subcategory:")
    print(df["subcategory"].value_counts())

    print("\nAverage price per category:")
    print(df.groupby("category")["price_clean"].mean())

    print("\nTop 5 expensive products:")
    print(df.sort_values("price_clean", ascending=False).head(5))


if __name__ == "__main__":
    main()