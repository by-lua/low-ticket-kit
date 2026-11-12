-- D1 schema for the checkout (orders, processed webhook events, delivery/tracking logs).
CREATE TABLE IF NOT EXISTS orders (
  id TEXT PRIMARY KEY,
  payment_intent TEXT,
  data TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_orders_payment_intent ON orders (payment_intent);
CREATE TABLE IF NOT EXISTS events (
  id TEXT PRIMARY KEY,
  at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  at TEXT NOT NULL,
  data TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_logs_name ON logs (name, id);
