import { NextResponse } from "next/server";
import { currentUser } from "@/lib/auth";
import { createOrder, getLead, listOrders, orderSkus } from "@/lib/db";
import { CURRENCY, siteUrl, mpPreference } from "@/lib/mp";
import { country } from "@/lib/country";
import { quoteAddons, BUMP_SKUS } from "@/lib/pricing";
import { createOxxoCharge, createSpeiCharge, XpagError, type XpagCharge } from "@/lib/xpag";

export const runtime = "nodejs";

/**
 * Compra de add-ons SUELTOS desde el panel, para quien ya tiene el núcleo y
 * le faltan uno o más bumps. Es una ruta APARTE de `/api/checkout` a propósito:
 * el checkout principal tiene un `yaPago` que bloquea cualquier orden nueva en
 * cuanto el lead tiene una aprobada — correcto para el flujo de venta, pero
 * acá es justo lo que hay que sortear (ella YA tiene una aprobada, por eso
 * está en el panel). Tocar esa condición en el checkout principal para
 * "hacer una excepción" es el camino directo a romper la protección contra
 * doble cobro del núcleo — mejor una ruta chica y auditable que una excepción
 * escondida en la ruta que sí mueve la mayoría de la plata del sitio.
 *
 * `applyPaymentStatus` (fulfill.ts) ya tiene el guard que hace esto seguro:
 * sólo agenda la entrega de la guía completa cuando la orden incluye "core".
 * Una orden de acá nunca lleva "core", así que aprobarla no reenvía nada del
 * núcleo — sólo lo que se compró.
 */
export async function POST(request: Request) {
  const user = await currentUser();
  if (!user) return NextResponse.json({ error: "No autenticado." }, { status: 401 });

  const lead = await getLead(user.leadId);
  if (!lead) return NextResponse.json({ error: "Lead no encontrado." }, { status: 404 });

  const ordenes = await listOrders();
  const aprobadas = ordenes.filter((o) => o.leadId === lead.id && o.status === "approved");
  const tieneCore = aprobadas.some((o) => orderSkus(o).includes("core"));
  if (!tieneCore) {
    // Sin el núcleo comprado, esto no es "sumar un add-on" — es un checkout
    // normal, que ya existe en /checkout. No duplicar ese camino acá.
    return NextResponse.json({ error: "Comprá primero El Número Maestro." }, { status: 403 });
  }

  const yaComprados = new Set(aprobadas.flatMap((o) => orderSkus(o)));

  const body = (await request.json().catch(() => null)) as { skus?: unknown } | null;
  const pedidos = Array.isArray(body?.skus) ? body.skus : [];
  // Sólo bumps válidos que todavía no tiene — pedir de nuevo algo que ya
  // compró le cobraría dos veces el mismo add-on.
  const skus = pedidos.filter(
    (s): s is string => typeof s === "string" && BUMP_SKUS.includes(s as never) && !yaComprados.has(s),
  );
  if (skus.length === 0) {
    return NextResponse.json({ error: "Nada para comprar." }, { status: 400 });
  }

  const { lines, total } = quoteAddons(skus);
  const amount = total;

  const order = await createOrder({
    leadId: lead.id,
    status: "pending",
    amount,
    currency: CURRENCY,
    source: "site",
    items: lines.map((l) => ({ sku: l.sku, title: l.title, amount: l.price })),
    email: lead.email,
    fullName: lead.name,
  });

  const base = siteUrl();
  const payerEmail = lead.email;

  if (country.gateway === "xpag") {
    const metodo = body && typeof (body as { method?: unknown }).method === "string" && (body as { method?: string }).method === "oxxo" ? "oxxo" : "spei";
    const secret = process.env.XPAG_WEBHOOK_SECRET;
    const webhookUrl = `${base}/api/webhook/xpag${secret ? `?k=${encodeURIComponent(secret)}` : ""}`;

    let charge: XpagCharge;
    try {
      const input = {
        externalId: `${order.id}:${metodo}`,
        amount,
        webhookUrl,
        payer: { name: lead.name, email: payerEmail ?? "" },
      };
      charge = metodo === "oxxo" ? await createOxxoCharge(input) : await createSpeiCharge(input);
    } catch (err) {
      const code = err instanceof XpagError ? err.code : "desconocido";
      console.error(`[panel/comprar] XPag falló (${code}):`, err);
      return NextResponse.json(
        { error: "No pudimos generar tu pago. Escribinos por soporte.", code, orderId: order.id },
        { status: 502 },
      );
    }

    return NextResponse.json({ orderId: order.id, amount, lines, charge });
  }

  let preferenceId: string | null = null;
  let initPoint: string | null = null;
  try {
    const pref = await mpPreference().create({
      body: {
        items: lines.map((line) => ({
          id: `${order.id}:${line.sku}`,
          title: line.title,
          description: line.title,
          category_id: "services",
          quantity: 1,
          unit_price: line.price,
          currency_id: CURRENCY,
        })),
        payer: {
          ...(payerEmail ? { email: payerEmail } : {}),
        },
        external_reference: order.id,
        back_urls: {
          success: `${base}/panel?comprado=${lines.map((l) => l.sku).join(",")}`,
          failure: `${base}/panel`,
          pending: `${base}/panel`,
        },
        auto_return: "approved",
        statement_descriptor: "LACIFRA",
        payment_methods: {
          excluded_payment_types: [{ id: "ticket" }, { id: "atm" }],
        },
      },
    });
    preferenceId = pref.id ?? null;
    initPoint =
      (process.env.MP_MODE === "production" ? pref.init_point : pref.sandbox_init_point) ??
      pref.init_point ??
      null;
  } catch (err) {
    console.error("[panel/comprar] falha ao criar preference MP:", err);
    return NextResponse.json(
      { error: "No pudimos abrir el pago. Probá de nuevo en unos minutos." },
      { status: 502 },
    );
  }

  return NextResponse.json({ orderId: order.id, amount, lines, preferenceId, initPoint });
}
