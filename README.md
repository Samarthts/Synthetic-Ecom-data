# E-Commerce Data Pipeline Project

A complete data pipeline project using Python, SQLite, and SQL for generating synthetic e-commerce data, managing it in a database, and performing analytical queries.

## Project Overview

This project demonstrates:
- **Data Generation**: Creating realistic synthetic e-commerce data using Python Faker
- **Database Management**: Setting up and managing SQLite database
- **SQL Queries**: Writing complex queries with JOINs and aggregations

## Project Structure

```
ecommerce-data-pipeline/
├── generate_ecommerce_data.py   # Generate synthetic data
├── create_database.py            # Create database and import data
├── query_database.py             # Execute SQL queries
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate Synthetic Data

Run the data generation script to create CSV files with synthetic e-commerce data:

```bash
python generate_ecommerce_data.py
```

This will generate:
- `customers.csv` (100 records)
- `categories.csv` (10 records)
- `products.csv` (50 records)
- `orders.csv` (200 records)
- `order_items.csv` (500 records)

### 3. Create Database and Import Data

Create the SQLite database and import data from CSV files:

```bash
python create_database.py
```

This creates `ecommerce.db` with 5 tables and imports all data.

### 4. Execute Queries

Run SQL queries to analyze the data:

```bash
python query_database.py
```

This generates 5 output CSV files with analytical results.

## Data Schema

### customers
- customer_id (Primary Key)
- customer_name
- email (Unique)
- phone
- address
- city
- country
- registration_date

### categories
- category_id (Primary Key)
- category_name
- description

### products
- product_id (Primary Key)
- product_name
- category_id (Foreign Key)
- price
- stock_quantity
- description

### orders
- order_id (Primary Key)
- customer_id (Foreign Key)
- order_date
- status (Pending, Shipped, Delivered, Cancelled)

### order_items
- order_item_id (Primary Key)
- order_id (Foreign Key)
- product_id (Foreign Key)
- quantity
- unit_price
- total_price

## Queries Included

1. **Customer Orders Summary** - Total orders per customer
2. **Detailed Order Information** - Complete order details with products
3. **Sales by Category** - Performance metrics per category
4. **Top Customers** - Best customers by spending
5. **Product Performance** - Sales metrics per product

## Output Files

After running the queries, you'll get:
- `output_customer_orders.csv`
- `output_order_details.csv`
- `output_sales_by_category.csv`
- `output_top_customers.csv`
- `output_product_performance.csv`

## Requirements

- Python 3.7+
- faker
- pandas

## Author

Created for the Cursor IDE A-SDLC Exercise

## License

MIT License
