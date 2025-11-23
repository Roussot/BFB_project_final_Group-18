-- Migration sample: insert sample data into SQLite for demonstration

INSERT INTO users (id, name, email, password, role) VALUES ('u_farmer','Ama Farmer','farmer@example.com','pass123','farmer');
INSERT INTO users (id, name, email, password, role) VALUES ('u_buyer','Bongi Buyer','buyer@example.com','pass123','buyer');
INSERT INTO users (id, name, email, password, role) VALUES ('u_dist','Dumi Logistics','dist@example.com','pass123','distributor');

INSERT INTO stock (id, farmer_id, crop, variety, qty_kg, location, harvest_date, price_per_kg, status) VALUES ('s1','u_farmer','Tomatoes','Roma',100,'North','2025-10-01',12.5,'PUBLISHED');

INSERT INTO orders (id, stock_id, buyer_id, qty_kg, price_per_kg, total, status, capacity_ok) VALUES ('o1','s1','u_buyer',20,12.5,250,'PENDING_CAPACITY',0);

INSERT INTO logistics (id, order_id, mode, cost, carrier, status) VALUES ('l1','o1','buyer',0,'Buyer Transport','SCHEDULED');
