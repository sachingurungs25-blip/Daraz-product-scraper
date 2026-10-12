# Daraz Nepal Product Scraper

A Python web scraping project that collects product information from Daraz Nepal and stores the results in a MariaDB database.

The project demonstrates HTTP requests, JSON data extraction, data cleaning, duplicate handling, relational database integration, and environment-based configuration.

## Features

- Extracts product names, product URLs, prices, and review counts.
- Collects up to 100 unique products per run.
- Stores product records in database.
- Prevents duplicate records using unique product URLs.
- Updates existing product information when a product is scraped again.
- Uses environment variables to keep database configuration separate from source code.
- Includes an SQL schema for setting up the database.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Scraping logic and data processing |
| Requests | Sends HTTP requests to Daraz |
| Database | Stores the collected product records |
| MySQL Connector/Python | Connects Python to Database |
| python-dotenv | Loads database configuration from `.env` |
| Git and GitHub | Version control and project hosting |

## Project Structure

```text
daraz-product-scraper/
├── scraper.py          # Fetches and processes product data
├── database.py         # Database connection configuration
├── schema.sql          # Database and table creation script
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
├── .env.example        # Example environment configuration
└── .gitignore          # Excludes local and sensitive files
```

## Prerequisites

Before running the project, ensure you have:

- Python installed.
- Git installed (optional, if you download the source as a ZIP).
- XAMPP or another MariaDB/MySQL installation.
- An internet connection.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/sachingurungs25-blip/Daraz-product-scraper.git
cd daraz-product-scraper
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the environment's Python directly using `.venv\Scripts\python.exe`.

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start MariaDB

If you use XAMPP, open the XAMPP Control Panel and start MySQL. In XAMPP, this service commonly runs MariaDB.

### 5. Create the database and table

Open phpMyAdmin or a MariaDB/MySQL client and execute the SQL statements in `schema.sql`.
Or, import the schema.sql from import tab in phpMyAdmin.

This creates the `daraz_scraper` database and its `products` table.

### 6. Configure environment variables

Copy `.env.example` to `.env` and adjust the values to match your local database configuration.

Example `.env.example`:

```dotenv
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=daraz_scraper
DB_USER=root
DB_PASSWORD=
```

Set `DB_PASSWORD` to your own database password if required. 

### 7. Run the scraper

```bash
python scraper.py
```

The scraper requests product listing data, extracts the required fields, removes duplicate URLs, and saves the collected records to database.

## Database Schema

The `products` table contains the following columns:

| Column | Type | Description |
|---|---|---|
| `id` | INT | Auto-incrementing primary key |
| `product_name` | VARCHAR(500) | Product name |
| `product_url` | VARCHAR(2048) | Product URL; unique constraint prevents duplicate URLs |
| `price` | DECIMAL(12,2) | Product price |
| `ratings_count` | INT UNSIGNED | Number of product reviews, when available |
| `scraped_at` | TIMESTAMP | Time the record was initially inserted |

The `ratings_count` field represents the review count returned by the listing data. It is not the product's average star rating.

## How It Works

1. **Request:** The scraper sends HTTP requests to Daraz Nepal's product listing endpoint using the Requests library.
2. **Extraction:** It reads the JSON response and extracts product information from the `mods.listItems` array.
3. **Data cleaning:** It normalises product URLs, converts prices into decimal values, and converts review counts into integers where available.
4. **Pagination:** It requests successive listing pages until it collects 100 unique products or reaches the configured page limit.
5. **Deduplication:** It uses product URLs to identify unique products.
6. **Database storage:** It inserts the collected records into database. If a URL already exists, the database operation updates the existing product's name, price, and review count.

A short delay between page requests helps avoid sending requests too rapidly.

## Example Output

A successful run in the development environment produced output similar to:

```text
Page 1: 40 returned, 40 new, 40 unique collected
Page 2: 40 returned, 40 new, 80 unique collected
Page 3: 40 returned, 20 new, 100 unique collected

Total unique products collected: 100
Saved 100 products to Database.
```

These figures describe a previous test run. Results may vary depending on the listing response, available products, and duplicate records.

## Verify the Results

Run the following SQL in phpMyAdmin or your SQL client:

```sql
USE daraz_scraper;

SELECT COUNT(*) AS total_products
FROM products;

SELECT product_name, product_url, price, ratings_count, scraped_at
FROM products
ORDER BY id DESC
LIMIT 10;
```

The first query checks the number of stored product records. The second displays a sample of the data.

## Challenges and Solutions

| Challenge | Approach |
|---|---|
| Extracting structured product data | Inspected the listing response and used its JSON product array |
| Handling duplicate products | Used unique product URLs and database upsert logic |
| Cleaning field values | Normalised URLs and converted price and review-count values to suitable data types |
| Separating credentials from code | Loaded database settings from environment variables |
| Making the project reproducible | Added `requirements.txt`, .env.example and `schema.sql` for setup |

## Limitations

- The current implementation uses a configured search query for men's shoes. It should not be treated as a complete catalogue of every product in a Daraz category.
- Listing responses and fields may change, requiring scraper maintenance.
- Product prices and review counts can change over time.
- Some products may not provide a review count.
- The scraper depends on network access and Daraz's listing endpoint remaining accessible.
- This project is intended for learning and evaluation, not high-volume scraping.

## Responsible Use

Use reasonable request intervals and avoid excessive traffic. Before running the scraper, review Daraz's applicable terms, access restrictions, and relevant policies. Do not attempt to bypass access controls or technical restrictions.

## Author

**Sachin Gurung**

## Disclaimer

This project is intended for educational and demonstration purposes. Daraz Nepal is a third-party platform; this project is not affiliated with or endorsed by Daraz.