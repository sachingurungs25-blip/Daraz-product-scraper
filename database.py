import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "daraz_scraper"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
    )


def save_products(products):
    if not products:
        print("No products to save.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    sql = """
        INSERT INTO products
            (product_name, product_url, price, ratings_count)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            product_name = VALUES(product_name),
            price = VALUES(price),
            ratings_count = VALUES(ratings_count)
    """

    values = [
        (
            product["product_name"],
            product["product_url"],
            product["price"],
            product["ratings_count"],
        )
        for product in products
    ]

    try:
        cursor.executemany(sql, values)
        connection.commit()
        print(f"Saved {len(products)} products to Database.")
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    try:
        connection = get_connection()

        if connection.is_connected():
            print("Successfully connected to Database!")

        connection.close()

    except mysql.connector.Error as error:
        print(f"Database connection failed: {error}")