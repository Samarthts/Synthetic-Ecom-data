import sqlite3
import pandas as pd

def query_customer_orders():
    """Query to join customers, orders, and order_items tables"""
    conn = sqlite3.connect('ecommerce.db')

    query = '''
        SELECT 
            c.customer_name,
            c.email,
            o.order_id,
            o.order_date,
            o.status,
            SUM(oi.total_price) as order_total
        FROM customers c
        INNER JOIN orders o ON c.customer_id = o.customer_id
        INNER JOIN order_items oi ON o.order_id = oi.order_id
        GROUP BY c.customer_name, c.email, o.order_id, o.order_date, o.status
        ORDER BY o.order_date DESC
        LIMIT 20
    '''

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def query_order_details():
    """Complex query joining all tables for detailed order information"""
    conn = sqlite3.connect('ecommerce.db')

    query = '''
        SELECT 
            c.customer_name,
            c.city,
            c.country,
            o.order_id,
            o.order_date,
            o.status,
            p.product_name,
            cat.category_name,
            oi.quantity,
            oi.unit_price,
            oi.total_price
        FROM customers c
        INNER JOIN orders o ON c.customer_id = o.customer_id
        INNER JOIN order_items oi ON o.order_id = oi.order_id
        INNER JOIN products p ON oi.product_id = p.product_id
        INNER JOIN categories cat ON p.category_id = cat.category_id
        WHERE o.status = 'Delivered'
        ORDER BY o.order_date DESC
        LIMIT 50
    '''

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def query_sales_by_category():
    """Analyze sales performance by product category"""
    conn = sqlite3.connect('ecommerce.db')

    query = '''
        SELECT 
            cat.category_name,
            COUNT(DISTINCT o.order_id) as total_orders,
            COUNT(oi.order_item_id) as total_items_sold,
            SUM(oi.quantity) as total_quantity,
            ROUND(SUM(oi.total_price), 2) as total_revenue,
            ROUND(AVG(oi.unit_price), 2) as avg_product_price
        FROM categories cat
        INNER JOIN products p ON cat.category_id = p.category_id
        INNER JOIN order_items oi ON p.product_id = oi.product_id
        INNER JOIN orders o ON oi.order_id = o.order_id
        WHERE o.status IN ('Shipped', 'Delivered')
        GROUP BY cat.category_name
        ORDER BY total_revenue DESC
    '''

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def query_top_customers():
    """Identify top customers by total purchase amount"""
    conn = sqlite3.connect('ecommerce.db')

    query = '''
        SELECT 
            c.customer_name,
            c.email,
            c.city,
            COUNT(DISTINCT o.order_id) as total_orders,
            SUM(oi.quantity) as total_items_purchased,
            ROUND(SUM(oi.total_price), 2) as total_spent
        FROM customers c
        INNER JOIN orders o ON c.customer_id = o.customer_id
        INNER JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.status != 'Cancelled'
        GROUP BY c.customer_id, c.customer_name, c.email, c.city
        HAVING total_spent > 100
        ORDER BY total_spent DESC
        LIMIT 10
    '''

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def query_product_performance():
    """Show all products including those never ordered"""
    conn = sqlite3.connect('ecommerce.db')

    query = '''
        SELECT 
            p.product_id,
            p.product_name,
            cat.category_name,
            p.price,
            p.stock_quantity,
            COALESCE(SUM(oi.quantity), 0) as times_ordered,
            COALESCE(ROUND(SUM(oi.total_price), 2), 0) as total_revenue
        FROM products p
        LEFT JOIN categories cat ON p.category_id = cat.category_id
        LEFT JOIN order_items oi ON p.product_id = oi.product_id
        GROUP BY p.product_id, p.product_name, cat.category_name, p.price, p.stock_quantity
        ORDER BY times_ordered DESC
    '''

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def main():
    """Execute all queries and save results"""
    print("Executing SQL queries on e-commerce database...\n")

    # Query 1: Customer Orders
    print("=" * 70)
    print("QUERY 1: Customer Orders Summary")
    print("=" * 70)
    df1 = query_customer_orders()
    print(df1.to_string())
    df1.to_csv('output_customer_orders.csv', index=False)
    print(f"\n✓ Saved to output_customer_orders.csv\n")

    # Query 2: Detailed Order Information
    print("=" * 70)
    print("QUERY 2: Detailed Order Information")
    print("=" * 70)
    df2 = query_order_details()
    print(df2.head(10).to_string())
    df2.to_csv('output_order_details.csv', index=False)
    print(f"\n✓ Saved to output_order_details.csv\n")

    # Query 3: Sales by Category
    print("=" * 70)
    print("QUERY 3: Sales Performance by Category")
    print("=" * 70)
    df3 = query_sales_by_category()
    print(df3.to_string())
    df3.to_csv('output_sales_by_category.csv', index=False)
    print(f"\n✓ Saved to output_sales_by_category.csv\n")

    # Query 4: Top Customers
    print("=" * 70)
    print("QUERY 4: Top 10 Customers by Total Spending")
    print("=" * 70)
    df4 = query_top_customers()
    print(df4.to_string())
    df4.to_csv('output_top_customers.csv', index=False)
    print(f"\n✓ Saved to output_top_customers.csv\n")

    # Query 5: Product Performance
    print("=" * 70)
    print("QUERY 5: Product Performance Analysis")
    print("=" * 70)
    df5 = query_product_performance()
    print(df5.head(15).to_string())
    df5.to_csv('output_product_performance.csv', index=False)
    print(f"\n✓ Saved to output_product_performance.csv\n")

    print("=" * 70)
    print("✓ All queries executed successfully!")
    print("=" * 70)

if __name__ == '__main__':
    main()
