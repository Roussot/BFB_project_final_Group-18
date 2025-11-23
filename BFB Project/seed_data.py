import sqlite3
import uuid
from datetime import datetime, timedelta
import os

DATABASE = 'agrimarket.db'

def init_database():
    """Initialize database schema"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock (
            id TEXT PRIMARY KEY,
            farmer_id TEXT NOT NULL,
            crop TEXT NOT NULL,
            variety TEXT,
            qty_kg INTEGER NOT NULL,
            location TEXT,
            harvest_date TEXT,
            price_per_kg REAL,
            status TEXT,
            FOREIGN KEY(farmer_id) REFERENCES users(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id TEXT PRIMARY KEY,
            stock_id TEXT NOT NULL,
            buyer_id TEXT NOT NULL,
            qty_kg INTEGER NOT NULL,
            price_per_kg REAL,
            total REAL,
            status TEXT,
            capacity_ok INTEGER,
            logistics_id TEXT,
            created_at TEXT,
            FOREIGN KEY(stock_id) REFERENCES stock(id),
            FOREIGN KEY(buyer_id) REFERENCES users(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logistics (
            id TEXT PRIMARY KEY,
            order_id TEXT NOT NULL,
            mode TEXT,
            cost REAL,
            carrier TEXT,
            status TEXT,
            discount REAL,
            FOREIGN KEY(order_id) REFERENCES orders(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Database schema initialized.")

def seed_database():
    """Populate database with sample data"""
    # Initialize database first
    init_database()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Check if data already exists
    existing_users = cursor.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    if existing_users > 0:
        print("Database already contains data. Skipping seed.")
        conn.close()
        return

    print("Seeding database with sample data...")

    # Create users
    users = [
        ('u_farmer1', 'Ama Farmer', 'farmer@example.com', 'pass123', 'farmer'),
        ('u_farmer2', 'Thabo Mthembu', 'thabo@example.com', 'pass123', 'farmer'),
        ('u_buyer1', 'Bongi Buyer', 'buyer@example.com', 'pass123', 'buyer'),
        ('u_buyer2', 'Sarah Johnson', 'sarah@example.com', 'pass123', 'buyer'),
        ('u_dist1', 'Dumi Logistics', 'dist@example.com', 'pass123', 'distributor'),
    ]

    for user in users:
        cursor.execute(
            'INSERT INTO users (id, name, email, password, role) VALUES (?, ?, ?, ?, ?)',
            user
        )

    print(f"Created {len(users)} users")

    # Create stock items
    stock_items = [
        ('s_001', 'u_farmer1', 'Tomatoes', 'Roma', 500, 'North', '2025-01-15', 25.50, 'available'),
        ('s_002', 'u_farmer1', 'Potatoes', 'Russet', 800, 'North', '2025-01-10', 18.00, 'available'),
        ('s_003', 'u_farmer2', 'Maize', 'Yellow', 1200, 'South', '2025-01-20', 15.75, 'available'),
        ('s_004', 'u_farmer2', 'Cabbage', 'Green', 300, 'South', '2025-01-18', 22.00, 'available'),
        ('s_005', 'u_farmer1', 'Carrots', 'Orange', 450, 'North', '2025-01-12', 20.50, 'available'),
        ('s_006', 'u_farmer2', 'Onions', 'Red', 600, 'East', '2025-01-14', 19.00, 'available'),
        ('s_007', 'u_farmer1', 'Spinach', 'Baby', 200, 'West', '2025-01-22', 35.00, 'available'),
        ('s_008', 'u_farmer2', 'Butternut', 'Local', 400, 'South', '2025-01-16', 28.50, 'available'),
    ]

    for stock in stock_items:
        cursor.execute(
            '''INSERT INTO stock (id, farmer_id, crop, variety, qty_kg, location,
               harvest_date, price_per_kg, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            stock
        )

    print(f"Created {len(stock_items)} stock items")

    # Create some orders
    orders = [
        ('o_001', 's_001', 'u_buyer1', 100, 25.50, 2550.00, 'DELIVERED', 1, None, '2025-01-16T10:30:00'),
        ('o_002', 's_002', 'u_buyer2', 200, 18.00, 3600.00, 'IN_TRANSIT', 1, None, '2025-01-17T14:20:00'),
        ('o_003', 's_003', 'u_buyer1', 300, 15.75, 4725.00, 'DELIVERED', 1, None, '2025-01-18T09:15:00'),
        ('o_004', 's_004', 'u_buyer2', 50, 22.00, 1100.00, 'READY_FOR_LOGISTICS', 1, None, '2025-01-19T11:45:00'),
        ('o_005', 's_005', 'u_buyer1', 150, 20.50, 3075.00, 'DELIVERED', 1, None, '2025-01-20T16:00:00'),
    ]

    for order in orders:
        cursor.execute(
            '''INSERT INTO orders (id, stock_id, buyer_id, qty_kg, price_per_kg,
               total, status, capacity_ok, logistics_id, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            order
        )

    print(f"Created {len(orders)} orders")

    # Create logistics records for some orders
    logistics = [
        ('l_001', 'o_001', 'buyer', 0, 'Buyer Transport', 'DELIVERED', 0.05),
        ('l_002', 'o_002', 'external', 250.00, 'Express Logistics SA', 'IN_TRANSIT', 0),
        ('l_003', 'o_003', 'buyer', 0, 'Buyer Transport', 'DELIVERED', 0.05),
        ('l_004', 'o_005', 'external', 180.00, 'Swift Couriers', 'DELIVERED', 0),
    ]

    for log in logistics:
        cursor.execute(
            '''INSERT INTO logistics (id, order_id, mode, cost, carrier, status, discount)
               VALUES (?, ?, ?, ?, ?, ?, ?)''',
            log
        )

    # Update orders with logistics_id
    cursor.execute("UPDATE orders SET logistics_id = 'l_001' WHERE id = 'o_001'")
    cursor.execute("UPDATE orders SET logistics_id = 'l_002' WHERE id = 'o_002'")
    cursor.execute("UPDATE orders SET logistics_id = 'l_003' WHERE id = 'o_003'")
    cursor.execute("UPDATE orders SET logistics_id = 'l_004' WHERE id = 'o_005'")

    print(f"Created {len(logistics)} logistics records")

    conn.commit()
    conn.close()

    print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()
