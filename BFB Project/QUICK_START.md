# Quick Start Guide

## Installation (2 minutes)

1. **Install Flask** (if not already installed):
   ```bash
   pip install Flask flask-cors
   ```

   Or use the requirements file:
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize Database**:
   ```bash
   python seed_data.py
   ```

   You should see:
   ```
   Database schema initialized.
   Seeding database with sample data...
   Created 5 users
   Created 8 stock items
   Created 5 orders
   Created 4 logistics records
   Database seeded successfully!
   ```

3. **Start the Server**:
   ```bash
   python app.py
   ```

   You should see:
   ```
   * Running on http://0.0.0.0:5000
   * Debug mode: on
   ```

4. **Open Browser**:
   - Navigate to: `http://localhost:5000`
   - You should see the Agrimarket landing page

## Testing the Application

### 1. View Marketplace
- Click "Marketplace" in navigation
- Browse available stock items
- Try the search and filter features
- Place an order (enter quantity and click "Order")

### 2. Upload Stock (as Farmer)
- Click "Upload Stock"
- Fill in the form:
  - Crop: Tomatoes
  - Quantity: 100
  - Harvest date: Any recent date
  - Location: North
  - Price: 25.00
  - Variety: Roma (optional)
- Click "Suggest Price" to see market average
- Click "Publish" to add stock

### 3. View Analytics
- Click "Analytics" in navigation
- See real-time KPIs:
  - Kg delivered
  - Orders delivered
  - Logistics breakdown
  - Total revenue
  - Average prices by crop

### 4. Test API Endpoints

Open a new terminal and test the API:

```bash
# Get all stock
curl http://localhost:5000/api/stock

# Get all users
curl http://localhost:5000/api/users

# Get KPIs
curl http://localhost:5000/api/analytics/kpis

# Create new stock (POST)
curl -X POST http://localhost:5000/api/stock \
  -H "Content-Type: application/json" \
  -d '{
    "farmer_id": "u_farmer1",
    "crop": "Carrots",
    "qty_kg": 200,
    "location": "East",
    "harvest_date": "2025-01-25",
    "price_per_kg": 22.50,
    "status": "available"
  }'
```

## Demo Credentials

Login with these credentials (if you implement login functionality):

| Email | Password | Role |
|-------|----------|------|
| farmer@example.com | pass123 | Farmer |
| buyer@example.com | pass123 | Buyer |
| dist@example.com | pass123 | Distributor |

## Troubleshooting

### Port Already in Use
If you see "Address already in use":
```bash
# On Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# On Mac/Linux
lsof -ti:5000 | xargs kill
```

### Module Not Found
If you see "ModuleNotFoundError: No module named 'flask'":
```bash
pip install Flask flask-cors
```

### Database Errors
If you see database errors:
```bash
# Delete the database and recreate
del agrimarket.db  # Windows
rm agrimarket.db   # Mac/Linux

# Re-run seed script
python seed_data.py
```

## Next Steps

1. **Update README.md** with your team member details
2. **Make individual commits** (each team member)
3. **Test all features** thoroughly
4. **Deploy to hosting service** (see DEPLOYMENT.md)
5. **Submit the hosted link** via ClickUp

## Project Structure Quick Reference

```
app.py              → Flask backend with all API endpoints
seed_data.py        → Database initialization and sample data
assets/api.js       → Frontend API client
marketplace.html    → Browse and order stock
farmer-upload.html  → Farmers upload their produce
analytics.html      → KPIs and metrics dashboard
```

## API Endpoints Quick Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/users` | GET | Get all users |
| `/api/users/<id>` | GET | Get user by ID |
| `/api/users` | POST | Create user |
| `/api/users/<id>` | PUT | Update user |
| `/api/stock` | GET | Get all stock |
| `/api/stock/<id>` | GET | Get stock by ID |
| `/api/stock` | POST | Create stock |
| `/api/stock/<id>` | PUT | Update stock |
| `/api/orders` | GET | Get all orders |
| `/api/orders/<id>` | GET | Get order by ID |
| `/api/orders` | POST | Create order |
| `/api/orders/<id>` | PUT | Update order |
| `/api/logistics` | GET | Get all logistics |
| `/api/logistics` | POST | Create logistics |
| `/api/logistics/<id>` | PUT | Update logistics |
| `/api/analytics/kpis` | GET | Get KPIs and metrics |

## Support

For issues or questions:
1. Check PROJECT_SUMMARY.md for detailed documentation
2. Review DEPLOYMENT.md for hosting instructions
3. Consult README.md for comprehensive setup guide
