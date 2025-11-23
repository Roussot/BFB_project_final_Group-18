# ERD (Entity Relationship Diagram) — Agrimarket (textual)

Entities:

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
