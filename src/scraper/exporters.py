# src/scraper/exporters.py
# Purpose: Save scraped product data to CSV and JSON files
import os
import csv
import json

def save_to_csv(products, filename="products.csv", folder="data"):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)
    if not products:
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=products[0].keys())
        writer.writeheader()
        writer.writerows(products)
    print(f"Saved {len(products)} products to {path}")

def save_to_json(products, filename="products.json", folder="data"):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=4)
    print(f"Saved {len(products)} products to {path}")