# Catalog Scraper 

## Project Purpose

This project scrapes the static e-commerce test site:
https://webscraper.io/test-sites/e-commerce/static

The scraper navigates categories and subcategories, handles pagination, extracts product details, and stores them in structured files.
After scraping, the data is cleaned and a summary report is generated.

The project demonstrates a simple **ETL pipeline (Extract, Transform, Load)** using Python.

---

## Project Setup Using uv

The project was initialized using **uv** to manage the Python environment.

Steps used:

```
uv init
uv add requests beautifulsoup4 pandas
```

This created the project environment and installed the required libraries.

---

## Installing Dependencies

To install all dependencies defined in the project:

```
uv sync
```

This installs all packages listed in `pyproject.toml`.

---

## How to Run the Scraper

Run the main scraper:

```
uv run python src/main.py
```

This will:

1. Crawl categories and subcategories
2. Handle pagination
3. Extract product information
4. Export scraped data to the `data` folder

Then run the transformation step:

```
python src/scraper/transform.py
```

This step:

* removes duplicate products
* cleans price values
* cleans text fields
* generates a summary report

---

## Branch Workflow Followed

The following branching workflow was used:

1. Created repository with **main**
2. Created **dev** branch
3. Created **feature/catalog-navigation**
4. Created **feature/product-details**
5. Merged both feature branches into **dev**
6. Created **fix/url-resolution**
7. Created **fix/deduplication**
8. Merged both fixes into **dev**
9. After final testing, merged **dev → main**

---

## Assumptions Made

* The website structure remains static.
* Product URLs are unique identifiers.
* All prices follow the `$` format.
* Some fields such as descriptions may be missing.

---

## Limitations

* No retry mechanism for failed requests
* No proxy or rate-limiting implementation
* Images are not downloaded (only product data is collected)
* Designed specifically for the provided test website

---

## Output Files

The scraper generates the following files inside the **data** folder:

* `products.csv` – raw scraped data
* `products.json` – raw data in JSON format
* `products_cleaned.csv` – cleaned dataset
* `category_summary.csv` – summary statistics by category

---

## Author

Minhal
