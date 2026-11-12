import { defineConfig } from "vite";
import { cloudflare } from "@cloudflare/vite-plugin";

// Cloudflare Vite plugin: runs the Worker in the Workers runtime (workerd) during `cf dev` and builds it for `cf deploy`.
// Static files come from ./public (Vite publicDir).
export default defineConfig({ plugins: [cloudflare()] });
