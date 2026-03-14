import pandas as pd
import os

def clean_and_summarize():

    data_folder = os.path.join(os.path.dirname(__file__), "..", "..", "data")
    data_folder = os.path.abspath(data_folder)

    input_file = os.path.join(data_folder, "products.csv")

    if not os.path.exists(input_file):
        print("products.csv not found")
        return

    df = pd.read_csv(input_file)
    print("Total rows:", len(df))

    # remove duplicates
    df = df.drop_duplicates(subset="url")

    # clean price
    df["price_clean"] = df["price"].str.replace("$","").str.replace(",","").astype(float)

    # save cleaned file
    cleaned_path = os.path.join(data_folder, "products_cleaned.csv")
    df.to_csv(cleaned_path, index=False)

    # summary
    summary = df.groupby(["category","subcategory"]).agg(
        total_products=("url","count"),
        avg_price=("price_clean","mean"),
        min_price=("price_clean","min"),
        max_price=("price_clean","max")
    ).reset_index()

    summary_path = os.path.join(data_folder, "category_summary.csv")
    summary.to_csv(summary_path, index=False)

    print("Files created in:", data_folder)
if __name__ == "__main__":
    clean_and_summarize()