// Node/Coolify store: orders, processed webhook events and logs in local files. Fine for test; for production on Coolify point DATA_DIR at a persistent volume (or swap for Postgres/SQLite).
import path from 'node:path';
import { readFile, writeFile, appendFile, mkdir } from 'node:fs/promises';

export class FileStore {
  constructor(dir) {
    this.dir = dir;
    this.file = path.join(dir, 'orders.json');
    this.orders = new Map();
    this.events = new Set();
  }
  async init() {
    await mkdir(this.dir, { recursive: true });
    try {
      const raw = JSON.parse(await readFile(this.file, 'utf8'));
      for (const o of raw.orders || []) this.orders.set(o.id, o);
      for (const e of raw.events || []) this.events.add(e);
    } catch { /* first run */ }
    return this;
  }
  async flush() { await writeFile(this.file, JSON.stringify({ orders: [...this.orders.values()], events: [...this.events] }, null, 2)); }
  async get(id) { return this.orders.get(id); }
  async put(order) { this.orders.set(order.id, order); await this.flush(); return order; }
  async findByIntent(pi) { return [...this.orders.values()].find((o) => o.paymentIntent === pi); }
  async seen(eventId) { if (this.events.has(eventId)) return true; this.events.add(eventId); await this.flush(); return false; }
  async log(name, payload) { await appendFile(path.join(this.dir, `${name}.jsonl`), JSON.stringify({ at: new Date().toISOString(), ...payload }) + '\n'); }
}
