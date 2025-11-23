-- SQLite schema for Agrimarket demo (for rubric demonstration)

CREATE TABLE users (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  role TEXT NOT NULL
);

CREATE TABLE stock (
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
);

CREATE TABLE orders (
  id TEXT PRIMARY KEY,
  stock_id TEXT NOT NULL,
  buyer_id TEXT NOT NULL,
  qty_kg INTEGER NOT NULL,
  price_per_kg REAL,
  total REAL,
  status TEXT,
  capacity_ok INTEGER,
  logistics_id TEXT,
  FOREIGN KEY(stock_id) REFERENCES stock(id),
  FOREIGN KEY(buyer_id) REFERENCES users(id)
);

CREATE TABLE logistics (
  id TEXT PRIMARY KEY,
  order_id TEXT NOT NULL,
  mode TEXT,
  cost REAL,
  carrier TEXT,
  status TEXT,
  FOREIGN KEY(order_id) REFERENCES orders(id)
);
