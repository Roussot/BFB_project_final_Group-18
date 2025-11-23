"""
Agrimarket Flask Backend Application
A REST API for managing agricultural supply chain operations
including stock management, orders, logistics, and analytics.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime
import uuid

# Initialize Flask application
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # Enable Cross-Origin Resource Sharing for frontend

DATABASE = 'agrimarket.db'

def get_db():
    """Create database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with schema"""
    with app.app_context():
        conn = get_db()
        cursor = conn.cursor()

        # Create tables
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

# ===== API ENDPOINTS =====

@app.route('/')
def index():
    """Serve the main index page"""
    return app.send_static_file('index.html')

# 1. USERS ENDPOINTS
@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    conn = get_db()
    users = conn.execute('SELECT id, name, email, role FROM users').fetchall()
    conn.close()
    return jsonify([dict(row) for row in users])

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID"""
    conn = get_db()
    user = conn.execute('SELECT id, name, email, role FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return jsonify(dict(user))
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.json
    user_id = str(uuid.uuid4())

    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO users (id, name, email, password, role) VALUES (?, ?, ?, ?, ?)',
            (user_id, data['name'], data['email'], data['password'], data['role'])
        )
        conn.commit()
        user = conn.execute('SELECT id, name, email, role FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        return jsonify(dict(user)), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Email already exists'}), 400

@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user information"""
    data = request.json
    conn = get_db()

    conn.execute(
        'UPDATE users SET name = ?, email = ? WHERE id = ?',
        (data.get('name'), data.get('email'), user_id)
    )
    conn.commit()

    user = conn.execute('SELECT id, name, email, role FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()

    if user:
        return jsonify(dict(user))
    return jsonify({'error': 'User not found'}), 404

# 2. STOCK ENDPOINTS
@app.route('/api/stock', methods=['GET'])
def get_stock():
    """Get all stock items with optional filters"""
    crop = request.args.get('crop', '')
    location = request.args.get('location', '')

    conn = get_db()
    query = 'SELECT * FROM stock WHERE qty_kg > 0'
    params = []

    if crop:
        query += ' AND LOWER(crop) LIKE ?'
        params.append(f'%{crop.lower()}%')

    if location:
        query += ' AND location = ?'
        params.append(location)

    stock_items = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(row) for row in stock_items])

@app.route('/api/stock/<stock_id>', methods=['GET'])
def get_stock_item(stock_id):
    """Get a specific stock item"""
    conn = get_db()
    stock = conn.execute('SELECT * FROM stock WHERE id = ?', (stock_id,)).fetchone()
    conn.close()

    if stock:
        return jsonify(dict(stock))
    return jsonify({'error': 'Stock not found'}), 404

@app.route('/api/stock', methods=['POST'])
def create_stock():
    """Create a new stock item"""
    data = request.json
    stock_id = str(uuid.uuid4())

    conn = get_db()
    conn.execute(
        '''INSERT INTO stock (id, farmer_id, crop, variety, qty_kg, location,
           harvest_date, price_per_kg, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (stock_id, data['farmer_id'], data['crop'], data.get('variety'),
         data['qty_kg'], data.get('location'), data.get('harvest_date'),
         data['price_per_kg'], data.get('status', 'available'))
    )
    conn.commit()

    stock = conn.execute('SELECT * FROM stock WHERE id = ?', (stock_id,)).fetchone()
    conn.close()
    return jsonify(dict(stock)), 201

@app.route('/api/stock/<stock_id>', methods=['PUT'])
def update_stock(stock_id):
    """Update stock item"""
    data = request.json
    conn = get_db()

    conn.execute(
        '''UPDATE stock SET qty_kg = ?, price_per_kg = ?, status = ?
           WHERE id = ?''',
        (data.get('qty_kg'), data.get('price_per_kg'), data.get('status'), stock_id)
    )
    conn.commit()

    stock = conn.execute('SELECT * FROM stock WHERE id = ?', (stock_id,)).fetchone()
    conn.close()

    if stock:
        return jsonify(dict(stock))
    return jsonify({'error': 'Stock not found'}), 404

# 3. ORDERS ENDPOINTS
@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Get all orders"""
    buyer_id = request.args.get('buyer_id')

    conn = get_db()
    if buyer_id:
        orders = conn.execute('SELECT * FROM orders WHERE buyer_id = ?', (buyer_id,)).fetchall()
    else:
        orders = conn.execute('SELECT * FROM orders').fetchall()
    conn.close()

    return jsonify([dict(row) for row in orders])

@app.route('/api/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    """Get a specific order"""
    conn = get_db()
    order = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    conn.close()

    if order:
        return jsonify(dict(order))
    return jsonify({'error': 'Order not found'}), 404

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create a new order"""
    data = request.json
    order_id = str(uuid.uuid4())
    total = data['qty_kg'] * data['price_per_kg']

    conn = get_db()
    conn.execute(
        '''INSERT INTO orders (id, stock_id, buyer_id, qty_kg, price_per_kg,
           total, status, capacity_ok, logistics_id, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (order_id, data['stock_id'], data['buyer_id'], data['qty_kg'],
         data['price_per_kg'], total, data.get('status', 'PENDING_CAPACITY'),
         None, None, datetime.now().isoformat())
    )
    conn.commit()

    order = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    conn.close()
    return jsonify(dict(order)), 201

@app.route('/api/orders/<order_id>', methods=['PUT'])
def update_order(order_id):
    """Update order status"""
    data = request.json
    conn = get_db()

    # Build dynamic update query
    update_fields = []
    params = []

    if 'status' in data:
        update_fields.append('status = ?')
        params.append(data['status'])

    if 'capacity_ok' in data:
        update_fields.append('capacity_ok = ?')
        params.append(data['capacity_ok'])

    if 'logistics_id' in data:
        update_fields.append('logistics_id = ?')
        params.append(data['logistics_id'])

    params.append(order_id)

    if update_fields:
        query = f"UPDATE orders SET {', '.join(update_fields)} WHERE id = ?"
        conn.execute(query, params)
        conn.commit()

    order = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    conn.close()

    if order:
        return jsonify(dict(order))
    return jsonify({'error': 'Order not found'}), 404

# 4. LOGISTICS ENDPOINTS
@app.route('/api/logistics', methods=['GET'])
def get_logistics():
    """Get all logistics records"""
    conn = get_db()
    logistics = conn.execute('SELECT * FROM logistics').fetchall()
    conn.close()
    return jsonify([dict(row) for row in logistics])

@app.route('/api/logistics', methods=['POST'])
def create_logistics():
    """Create a logistics record"""
    data = request.json
    logistics_id = str(uuid.uuid4())

    conn = get_db()
    conn.execute(
        '''INSERT INTO logistics (id, order_id, mode, cost, carrier, status, discount)
           VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (logistics_id, data['order_id'], data['mode'], data.get('cost', 0),
         data.get('carrier'), data.get('status', 'SCHEDULED'), data.get('discount', 0))
    )
    conn.commit()

    # Update order with logistics_id
    conn.execute('UPDATE orders SET logistics_id = ?, status = ? WHERE id = ?',
                 (logistics_id, 'IN_TRANSIT', data['order_id']))
    conn.commit()

    logistics = conn.execute('SELECT * FROM logistics WHERE id = ?', (logistics_id,)).fetchone()
    conn.close()
    return jsonify(dict(logistics)), 201

@app.route('/api/logistics/<logistics_id>', methods=['PUT'])
def update_logistics(logistics_id):
    """Update logistics status"""
    data = request.json
    conn = get_db()

    conn.execute('UPDATE logistics SET status = ? WHERE id = ?',
                 (data.get('status'), logistics_id))
    conn.commit()

    logistics = conn.execute('SELECT * FROM logistics WHERE id = ?', (logistics_id,)).fetchone()
    conn.close()

    if logistics:
        return jsonify(dict(logistics))
    return jsonify({'error': 'Logistics record not found'}), 404

# 5. ANALYTICS/KPI ENDPOINT
@app.route('/api/analytics/kpis', methods=['GET'])
def get_kpis():
    """Get key performance indicators"""
    conn = get_db()

    # Total kg delivered
    kg_delivered = conn.execute(
        "SELECT COALESCE(SUM(qty_kg), 0) as total FROM orders WHERE status = 'DELIVERED'"
    ).fetchone()['total']

    # Orders delivered
    orders_delivered = conn.execute(
        "SELECT COUNT(*) as count FROM orders WHERE status = 'DELIVERED'"
    ).fetchone()['count']

    # Buyer-arranged logistics
    buyer_logistics = conn.execute(
        "SELECT COUNT(*) as count FROM logistics WHERE mode = 'buyer'"
    ).fetchone()['count']

    # External courier
    external_courier = conn.execute(
        "SELECT COUNT(*) as count FROM logistics WHERE mode = 'external'"
    ).fetchone()['count']

    # Total revenue
    total_revenue = conn.execute(
        "SELECT COALESCE(SUM(total), 0) as revenue FROM orders WHERE status = 'DELIVERED'"
    ).fetchone()['revenue']

    # Average price per crop
    avg_prices = conn.execute(
        "SELECT crop, AVG(price_per_kg) as avg_price FROM stock GROUP BY crop"
    ).fetchall()

    conn.close()

    return jsonify({
        'kg_delivered': kg_delivered,
        'orders_delivered': orders_delivered,
        'buyer_arranged_logistics': buyer_logistics,
        'external_courier': external_courier,
        'total_revenue': round(total_revenue, 2),
        'average_prices_by_crop': [dict(row) for row in avg_prices]
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Initialize database if it doesn't exist
    if not os.path.exists(DATABASE):
        init_db()

    app.run(debug=True, host='0.0.0.0', port=5000)
