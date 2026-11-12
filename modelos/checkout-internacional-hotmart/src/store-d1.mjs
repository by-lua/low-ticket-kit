// Cloudflare store: D1 (SQLite at the edge). Tables in migrations/0001_init.sql; the same statements run idempotently on first use
// (CREATE TABLE IF NOT EXISTS) so `cf dev` and a fresh database work without a separate migration step.
const SCHEMA = [
  'CREATE TABLE IF NOT EXISTS orders (id TEXT PRIMARY KEY, payment_intent TEXT, data TEXT NOT NULL, updated_at TEXT NOT NULL)',
  'CREATE INDEX IF NOT EXISTS idx_orders_payment_intent ON orders (payment_intent)',
  'CREATE TABLE IF NOT EXISTS events (id TEXT PRIMARY KEY, at TEXT NOT NULL)',
  'CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, at TEXT NOT NULL, data TEXT NOT NULL)',
  'CREATE INDEX IF NOT EXISTS idx_logs_name ON logs (name, id)',
];

export class D1Store {
  constructor(db) { this.db = db; this._ready = null; }
  ready() { return (this._ready ??= this.db.batch(SCHEMA.map((sql) => this.db.prepare(sql)))); }
  async get(id) {
    if (!id) return undefined;
    await this.ready();
    const row = await this.db.prepare('SELECT data FROM orders WHERE id = ?').bind(id).first();
    return row ? JSON.parse(row.data) : undefined;
  }
  async put(order) {
    await this.ready();
    // Plain positional placeholders keep the statement portable (D1 and node:sqlite); REPLACE rewrites the whole row.
    await this.db.prepare('INSERT OR REPLACE INTO orders (id, payment_intent, data, updated_at) VALUES (?, ?, ?, ?)')
      .bind(order.id, order.paymentIntent ?? null, JSON.stringify(order), new Date().toISOString()).run();
    return order;
  }
  async findByIntent(pi) {
    if (!pi) return undefined;
    await this.ready();
    const row = await this.db.prepare('SELECT data FROM orders WHERE payment_intent = ?').bind(pi).first();
    return row ? JSON.parse(row.data) : undefined;
  }
  /** true when the event was already processed (idempotent webhook). */
  async seen(eventId) {
    await this.ready();
    const res = await this.db.prepare('INSERT OR IGNORE INTO events (id, at) VALUES (?, ?)').bind(eventId, new Date().toISOString()).run();
    return (res.meta?.changes ?? 0) === 0;
  }
  async log(name, payload) {
    await this.ready();
    await this.db.prepare('INSERT INTO logs (name, at, data) VALUES (?, ?, ?)').bind(name, new Date().toISOString(), JSON.stringify(payload)).run();
  }
}
