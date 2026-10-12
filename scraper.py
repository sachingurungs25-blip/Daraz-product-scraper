
import time
from decimal import Decimal, InvalidOperation
from urllib.parse import urljoin

import requests
from database import save_products

BASE_URL = "https://www.daraz.com.np/catalog/"
TARGET_PRODUCTS = 100
MAX_PAGES = 5

PARAMS = {
    "ajax": "true",
    "q": "shoes for men",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.daraz.com.np/",
}


def extract_products(items):
    products = []

    for item in items:
        name = item.get("name")
        raw_url = item.get("itemUrl")
        raw_price = item.get("price")
        raw_reviews = item.get("review")

        if not name or not raw_url or raw_price is None:
            continue

        try:
            price = Decimal(str(raw_price).replace(",", ""))
            if not price.is_finite() or price < 0:
                continue
        except InvalidOperation:
            continue

        try:
            ratings_count = (
                int(raw_reviews)
                if raw_reviews not in (None, "")
                else None
            )
            if ratings_count is not None and ratings_count < 0:
                ratings_count = None
        except (TypeError, ValueError):
            ratings_count = None

        product_url = urljoin(
            "https://www.daraz.com.np",
            raw_url,
        )

        products.append({
            "product_name": name.strip(),
            "product_url": product_url,
            "price": price,
            "ratings_count": ratings_count,
        })

    return products


def scrape_products():
    unique_products = {}
    
    with requests.Session() as session:
        session.headers.update(HEADERS)

        for page in range(1, MAX_PAGES + 1):
            if len(unique_products) >= TARGET_PRODUCTS:
                break

            params = {
                **PARAMS,
                "page": page,
            }

            try:
                response = session.get(
                    BASE_URL,
                    params=params,
                    timeout=20,
                )
                response.raise_for_status()
                data = response.json()

            except (requests.RequestException, ValueError) as error:
                print(f"Page {page} failed: {error}")
                break

            items = data.get("mods", {}).get("listItems", [])

            if not isinstance(items, list) or not items:
                print(f"No products found on page {page}.")
                break

            new_count = 0

            for product in extract_products(items):
                key = product["product_url"]

                if key not in unique_products:
                    unique_products[key] = product
                    new_count += 1

                    if len(unique_products) >= TARGET_PRODUCTS:
                        break

            print(
                f"Page {page}: {len(items)} returned, "
                f"{new_count} new, "
                f"{len(unique_products)} unique collected"
            )

            if len(unique_products) >= TARGET_PRODUCTS:
                break

            # Pause between requests; do not retry access-denied responses.
            if page < MAX_PAGES:
                time.sleep(2)

    return list(unique_products.values())


if __name__ == "__main__":
    products = scrape_products()

    print(f"\nTotal unique products collected: {len(products)}")

    if products:
        save_products(products)
