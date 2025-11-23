# Agrimarket — Supply Chain Web Application

A full-stack farm-to-market supply chain platform connecting farmers, buyers, and logistics providers. This application streamlines agricultural supply chains by matching farm supply to real-time demand, improving pricing visibility, and coordinating delivery logistics.

## Team Members

| Name | Student ID |
|------|-----------|
| Chad de Weijer | u23585324 |
| Calum Le Roux | u23554429 |
| Alexandros Roussot | u23546493 |

## Task Allocation

- **Chad de Weijer**: Backend API development, database design and integration
- **Calum Le Roux**: Frontend development and API integration
- **Alexandros Roussot**: Testing, documentation, and deployment

## Project Structure

```
BFB Project/
├── app.py                 # Flask backend application
├── seed_data.py           # Database seeding script
├── requirements.txt       # Python dependencies
├── agrimarket.db         # SQLite database (generated)
├── index.html            # Landing page
├── marketplace.html      # Browse and order stock
├── farmer-upload.html    # Farmers upload stock
├── orders.html           # Order management
├── logistics.html        # Logistics coordination
├── analytics.html        # KPIs and analytics dashboard
├── login.html            # User login
├── register.html         # User registration
├── assets/
│   ├── api.js           # Frontend API client
│   ├── app.js           # Legacy frontend logic
│   ├── auth.js          # Authentication helpers
│   └── styles.css       # Custom styles
└── database/
    ├── schema.sql       # Database schema
    └── ERD.md          # Entity Relationship Diagram
```

## Technology Stack

**Backend:**
- Flask (Python web framework)
- SQLite (Database)
- Flask-CORS (Cross-Origin Resource Sharing)

**Frontend:**
- HTML5, CSS3, JavaScript (ES6+)
- Bootstrap 5.3.3 (UI framework)
- Fetch API (HTTP requests)

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository** (or download the project folder)
   ```bash
   cd "c:\Users\chadd\Downloads\BFB 321\BFB Project"
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize and seed the database**
   ```bash
   python seed_data.py
   ```

4. **Run the Flask server**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your browser and navigate to: `http://localhost:5000`
   - The Flask server serves both the API and frontend files

### Demo Users

| Email | Password | Role |
|-------|----------|------|
| farmer@example.com | pass123 | Farmer |
| buyer@example.com | pass123 | Buyer |
| dist@example.com | pass123 | Distributor |

## API Endpoints

The application implements the following REST API endpoints:

### Users
- `GET /api/users` - Get all users
- `GET /api/users/<id>` - Get user by ID
- `POST /api/users` - Create new user
- `PUT /api/users/<id>` - Update user

### Stock
- `GET /api/stock` - Get all stock (with optional filters: crop, location)
- `GET /api/stock/<id>` - Get stock item by ID
- `POST /api/stock` - Create new stock item
- `PUT /api/stock/<id>` - Update stock item

### Orders
- `GET /api/orders` - Get all orders (with optional filter: buyer_id)
- `GET /api/orders/<id>` - Get order by ID
- `POST /api/orders` - Create new order
- `PUT /api/orders/<id>` - Update order status

### Logistics
- `GET /api/logistics` - Get all logistics records
- `POST /api/logistics` - Create logistics record
- `PUT /api/logistics/<id>` - Update logistics status

### Analytics
- `GET /api/analytics/kpis` - Get key performance indicators including:
  - Kg delivered
  - Orders delivered
  - Logistics breakdown
  - Total revenue
  - Average prices by crop

## Features

1. **Marketplace**: Browse available stock with search and filter capabilities
2. **Stock Management**: Farmers can upload and manage their produce inventory
3. **Order Processing**: Create and track orders from creation to delivery
4. **Logistics Coordination**: Manage shipping and delivery options
5. **Analytics Dashboard**: Real-time KPIs and metrics visualization
6. **User Authentication**: Role-based access for farmers, buyers, and distributors

## Database Schema

The application uses SQLite with the following key entities:

- **users**: User accounts (farmers, buyers, distributors)
- **stock**: Farm produce inventory
- **orders**: Purchase orders
- **logistics**: Shipping and delivery information

See [database/ERD.md](database/ERD.md) for the complete entity relationship diagram.

## ERD (Entity Relationship Diagram)

The application uses the following entities (textual ERD):

- users (id PK)
	- id
	- name
	- email
	- password
	- role

- stock (id PK)
	- id
	- farmer_id (FK -> users.id)
	- crop
	- variety
	- qty_kg
	- location
	- harvest_date
	- price_per_kg
	- status

- orders (id PK)
	- id
	- stock_id (FK -> stock.id)
	- buyer_id (FK -> users.id)
	- qty_kg
	- price_per_kg
	- total
	- status
	- capacity_ok
	- logistics_id

- logistics (id PK)
	- id
	- order_id (FK -> orders.id)
	- mode
	- cost
	- carrier
	- status

Relationships:
- users 1---* stock (one farmer can list many stock items)
- stock 1---* orders (one stock listing can generate many orders)
- users 1---* orders (one buyer can place many orders)
- orders 1---1 logistics (each order may have associated logistics record)
