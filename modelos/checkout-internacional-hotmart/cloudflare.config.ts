// Cloudflare (cf CLI) configuration. Beta format: see https://developers.cloudflare.com/cf/projects/cloudflare-config/index.md
// Deploy only with the owner's Cloudflare account logged in (`cf auth whoami` must show HER account). Nothing here is deployed yet.
import { bindings, defineConfig } from "cf/config";
import * as entrypoint from "./src/worker.mjs" with { type: "cf-worker" };

export default defineConfig({
  worker: {
    name: "checkout-internacional", // rename per offer, e.g. "my-offer"
    // Public address: a NEW subdomain in a zone of the owner's account (HTTPS + Apple Pay domain). Without it, register a workers.dev subdomain.
    domains: ["checkout-my-offer.example.com"],
    workersDev: false,
    entrypoint,
    compatibilityDate: "2026-11-01",
    compatibilityFlags: ["nodejs_compat"],
    env: {
      DB: bindings.d1({ name: "checkout-db" }),
      OFFER_SLUG: bindings.text("my-offer-slug"),      // per offer
      OFFER_DESCRIPTION: bindings.text("My Offer"),   // shown on the Stripe/PayPal receipt
      BRAND: bindings.text("My Brand"),
      // Secrets: values come from .dev.vars locally (see .dev.vars.example) and from `cf deploy --secrets-file` / dashboard in production.
      STRIPE_SECRET_KEY: bindings.secret(),
      STRIPE_PUBLISHABLE_KEY: bindings.secret(),
      STRIPE_WEBHOOK_SECRET: bindings.secret(),
      PAYPAL_CLIENT_ID: bindings.secret(),
      PAYPAL_SECRET: bindings.secret(),
      // Optional (AGENTS.md §1c). Declared secrets become REQUIRED on deploy, so uncomment each one only when you have its value:
      // DELIVERY_WEBHOOK_URL: bindings.secret(), DELIVERY_WEBHOOK_SECRET: bindings.secret(),
      // TRACKEADOR_WEBHOOK_URL: bindings.secret(), TRACKEADOR_SECRET: bindings.secret(),
      // ADMIN_TOKEN: bindings.secret(),
    },
  },
});
