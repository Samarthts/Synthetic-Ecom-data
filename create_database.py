import sqlite3
import pandas as pd
import os

def create_connection(db_file):
    """Create a database connection to SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"✓ Connected to {db_file}")
        return conn
    except sqlite3.Error as e:
        print(f"✗ Error connecting to database: {e}")
    return conn

def create_tables(conn):
    """Create tables in the SQLite database"""
    cursor = conn.cursor()

    # Create customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            customer_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            address TEXT,
            city TEXT,
            country TEXT,
            registration_date DATE
        )
    ''')

    # Create categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY,
            category_name TEXT NOT NULL,
            description TEXT
        )
    ''')

    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category_id INTEGER,
            price REAL NOT NULL,
            stock_quantity INTEGER,
            description TEXT,
            FOREIGN KEY (category_id) REFERENCES categories (category_id)
        )
    ''')

    # Create orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            order_date DATETIME,
            status TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        )
    ''')

    # Create order_items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (order_id),
            FOREIGN KEY (product_id) REFERENCES products (product_id)
        )
    ''')

    conn.commit()
    print("✓ All tables created successfully")

def import_csv_to_table(conn, csv_file, table_name):
    """Import data from CSV file into SQLite table"""
    if not os.path.exists(csv_file):
        print(f"✗ Warning: {csv_file} not found")
        return

    try:
        df = pd.read_csv(csv_file)
        df.to_sql(table_name, conn, if_exists='append', index=False)
        print(f"✓ Imported {len(df)} rows from {csv_file} into {table_name}")
    except Exception as e:
        print(f"✗ Error importing {csv_file}: {e}")

def main():
    """Main function to create database and import data"""
    database = "ecommerce.db"

    # Create database connection
    conn = create_connection(database)

    if conn is not None:
        # Create tables
        create_tables(conn)

        # Import data from CSV files
        csv_files = {
            'customers.csv': 'customers',
            'categories.csv': 'categories',
            'products.csv': 'products',
            'orders.csv': 'orders',
            'order_items.csv': 'order_items'
        }

        print("\nImporting data...")
        for csv_file, table_name in csv_files.items():
            import_csv_to_table(conn, csv_file, table_name)

        # Verify data import
        print("\nVerifying data...")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table in tables:
            if table[0] != 'sqlite_sequence':
                cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                count = cursor.fetchone()[0]
                print(f"✓ {table[0]}: {count} rows")

        conn.close()
        print("\n✓ Database created and populated successfully!")
    else:
        print("✗ Error! Cannot create database connection.")

if __name__ == '__main__':
    main()
