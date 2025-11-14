from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta

fake = Faker()
Faker.seed(42)

def generate_customers(num_customers=100):
    """Generate synthetic customer data"""
    customers = []
    for i in range(num_customers):
        customer = {
            'customer_id': i + 1,
            'customer_name': fake.name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'address': fake.address().replace('\n', ', '),
            'city': fake.city(),
            'country': fake.country(),
            'registration_date': fake.date_between(start_date='-2y', end_date='today')
        }
        customers.append(customer)
    return pd.DataFrame(customers)

def generate_categories(num_categories=10):
    """Generate product categories"""
    categories = []
    category_names = [
        'Electronics', 'Clothing', 'Home & Garden', 'Sports & Outdoors',
        'Books', 'Toys & Games', 'Health & Beauty', 'Automotive',
        'Food & Beverages', 'Office Supplies'
    ]
    for i in range(min(num_categories, len(category_names))):
        category = {
            'category_id': i + 1,
            'category_name': category_names[i],
            'description': fake.sentence()
        }
        categories.append(category)
    return pd.DataFrame(categories)

def generate_products(num_products=50, num_categories=10):
    """Generate product data"""
    products = []
    for i in range(num_products):
        product = {
            'product_id': i + 1,
            'product_name': fake.catch_phrase(),
            'category_id': random.randint(1, num_categories),
            'price': round(random.uniform(5.0, 500.0), 2),
            'stock_quantity': random.randint(0, 200),
            'description': fake.text(max_nb_chars=200)
        }
        products.append(product)
    return pd.DataFrame(products)

def generate_orders(num_orders=200, num_customers=100):
    """Generate order data"""
    orders = []
    for i in range(num_orders):
        order = {
            'order_id': i + 1,
            'customer_id': random.randint(1, num_customers),
            'order_date': fake.date_time_between(start_date='-1y', end_date='now'),
            'status': random.choice(['Pending', 'Shipped', 'Delivered', 'Cancelled'])
        }
        orders.append(order)
    return pd.DataFrame(orders)

def generate_order_items(num_order_items=500, num_orders=200, num_products=50):
    """Generate order items data"""
    order_items = []
    for i in range(num_order_items):
        quantity = random.randint(1, 5)
        unit_price = round(random.uniform(5.0, 500.0), 2)
        order_item = {
            'order_item_id': i + 1,
            'order_id': random.randint(1, num_orders),
            'product_id': random.randint(1, num_products),
            'quantity': quantity,
            'unit_price': unit_price,
            'total_price': round(quantity * unit_price, 2)
        }
        order_items.append(order_item)
    return pd.DataFrame(order_items)

def main():
    """Main function to generate and save all data"""
    print("Generating synthetic e-commerce data...")

    # Generate data
    customers_df = generate_customers(100)
    categories_df = generate_categories(10)
    products_df = generate_products(50, 10)
    orders_df = generate_orders(200, 100)
    order_items_df = generate_order_items(500, 200, 50)

    # Save to CSV files
    customers_df.to_csv('customers.csv', index=False)
    categories_df.to_csv('categories.csv', index=False)
    products_df.to_csv('products.csv', index=False)
    orders_df.to_csv('orders.csv', index=False)
    order_items_df.to_csv('order_items.csv', index=False)

    print("✓ Synthetic e-commerce data generated successfully!")
    print(f"✓ Generated {len(customers_df)} customers")
    print(f"✓ Generated {len(categories_df)} categories")
    print(f"✓ Generated {len(products_df)} products")
    print(f"✓ Generated {len(orders_df)} orders")
    print(f"✓ Generated {len(order_items_df)} order items")

if __name__ == '__main__':
    main()
