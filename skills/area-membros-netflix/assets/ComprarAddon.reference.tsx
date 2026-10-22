"use client";

import { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { BUMP_DESCRIPTION, formatMoney, product, type Sku } from "@/lib/pricing";
import { country } from "@/lib/country";
import { t } from "@/lib/copy";

interface Props {
  skuPrincipal: Sku;
  /** Otros bumps que todavía le faltan — se ofrecen como opcionales en la misma compra. */
  otrosDisponibles: Sku[];
}

interface XpagChargeSpei {
  method: "SPEI";
  clabe: string;
  bankName: string;
  beneficiary: string;
  amount: number;
}

interface XpagChargeOxxo {
  method: "OXXO";
  reference: string;
  barcodeUrl?: string;
  amount: number;
}

type Estado =
  | { paso: "elegir" }
  | { paso: "enviando" }
  | { paso: "error"; mensaje: string }
  | { paso: "redirigiendo" }
  | { paso: "cobro-mx"; charge: XpagChargeSpei | XpagChargeOxxo };

/**
 * Compra de add-on suelto desde el panel — mismo look & feel exacto del
 * checkout principal (banner, card blanca, lista "Aprovechá y sumá" con la
 * misma clase de tarjeta), no una pantalla minimalista aparte. La única
 * diferencia real es que no hay línea del núcleo (ya lo tiene) y el bump
 * que la trajo entra pre-marcado.
 */
export default function ComprarAddon({ skuPrincipal, otrosDisponibles }: Props) {
  const [elegidos, setElegidos] = useState<Set<Sku>>(new Set([skuPrincipal]));
  const [estado, setEstado] = useState<Estado>({ paso: "elegir" });

  const principal = product(skuPrincipal);
  const todos = [skuPrincipal, ...otrosDisponibles];
  const total = [...elegidos].reduce((acc, s) => acc + product(s).price, 0);

  function toggle(sku: Sku) {
    if (sku === skuPrincipal) return; // el que la trajo hasta acá siempre va
    setElegidos((prev) => {
      const next = new Set(prev);
      if (next.has(sku)) next.delete(sku);
      else next.add(sku);
      return next;
    });
  }

  async function pagar(method?: "spei" | "oxxo") {
    setEstado({ paso: "enviando" });
    try {
      const res = await fetch("/api/panel/comprar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ skus: [...elegidos], method }),
      });
      const data = await res.json();
      if (!res.ok) {
        setEstado({ paso: "error", mensaje: data?.error ?? "No pudimos procesar la compra." });
        return;
      }
      if (data.initPoint) {
        setEstado({ paso: "redirigiendo" });
        window.location.href = data.initPoint;
        return;
      }
      if (data.charge) {
        setEstado({ paso: "cobro-mx", charge: data.charge });
        return;
      }
      setEstado({ paso: "error", mensaje: "Respuesta inesperada del servidor." });
    } catch {
      setEstado({ paso: "error", mensaje: "No pudimos conectar. Probá de nuevo." });
    }
  }

  if (estado.paso === "cobro-mx") {
    const { charge } = estado;
    return (
      <div className="min-h-screen bg-neutral-50">
        <div className="mx-auto w-full max-w-3xl px-4 py-10">
          <section className="rounded-2xl border border-gold/25 bg-white p-6 shadow-[0_20px_45px_-30px_rgba(42,22,8,0.35)] sm:p-10">
            <h1 className="text-xl font-bold" style={{ color: "var(--color-gold-deep)" }}>
              Tu pago
            </h1>
            {charge.method === "SPEI" ? (
              <div className="mt-4 rounded-xl border border-gold/25 bg-gold/5 p-5">
                <p className="text-sm text-neutral-600">Transferí por SPEI a esta CLABE:</p>
                <p className="mt-1 text-xl font-bold tracking-wide">{charge.clabe}</p>
                <p className="mt-2 text-sm text-neutral-500">
                  {charge.bankName} · {charge.beneficiary}
                </p>
                <p className="mt-3 text-lg font-semibold">{formatMoney(charge.amount)}</p>
              </div>
            ) : (
              <div className="mt-4 rounded-xl border border-gold/25 bg-gold/5 p-5">
                <p className="text-sm text-neutral-600">Pagá en efectivo en cualquier OXXO con esta referencia:</p>
                <p className="mt-1 text-xl font-bold tracking-wide">{charge.reference}</p>
                <p className="mt-3 text-lg font-semibold">{formatMoney(charge.amount)}</p>
              </div>
            )}
            <p className="mt-5 text-sm text-neutral-500">
              En cuanto se acredite el pago, el módulo se desbloquea solo en tu área.
            </p>
            <Link href="/panel" className="mt-6 inline-block text-sm text-neutral-500 underline">
              ← Volver a tu área
            </Link>
          </section>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-neutral-50">
      <div className="mx-auto w-full max-w-3xl px-4 py-6 sm:py-10">
        {/* Mismo banner del checkout principal — consistencia visual, no una
            pantalla aparte que parezca de otro sitio. */}
        <div className="relative aspect-[1672/941] w-full overflow-hidden rounded-t-2xl border border-b-0 border-gold/25 bg-neutral-900">
          <Image
            src={`/checkout/banner-${country.code}-desktop.jpg`}
            alt=""
            fill
            priority
            sizes="(min-width: 768px) 768px, 100vw"
            className="object-cover"
          />
        </div>

        <section className="rounded-b-2xl border border-t-0 border-gold/25 bg-white p-5 shadow-[0_20px_45px_-30px_rgba(42,22,8,0.35)] sm:p-8 md:p-10">
          <div className="mb-6 flex items-center justify-between gap-4 border-b border-black/10 pb-5">
            <div>
              <p className="text-lg font-bold sm:text-xl" style={{ color: "var(--color-gold-deep)" }}>
                {principal.title}
              </p>
              <p className="text-sm text-neutral-500">
                {t("Se suma a lo que ya compraste", "Se suma a lo que ya compraste")}
              </p>
            </div>
            <div className="text-right">
              <p className="text-sm text-neutral-400 line-through">{formatMoney(principal.compareAt)}</p>
              <p className="text-xl font-bold text-neutral-900 sm:text-2xl">{formatMoney(total)}</p>
            </div>
          </div>

          <div className="grid gap-6 md:grid-cols-[minmax(0,1fr)_20rem] md:items-start md:gap-8">
            <div className="grid gap-2">
              <p className="text-sm font-medium text-neutral-900">
                {t("Aprovechá y sumá:", "Aprovecha y suma:")}
              </p>
              {todos.map((sku) => {
                const p = product(sku);
                const elegido = elegidos.has(sku);
                const esPrincipal = sku === skuPrincipal;
                return (
                  <label
                    key={sku}
                    className={`flex items-start gap-3 rounded-xl border p-3.5 transition ${
                      elegido ? "border-gold bg-gold/10" : "border-emerald-200 bg-emerald-50/50 hover:border-emerald-300"
                    } ${esPrincipal ? "cursor-default" : "cursor-pointer"}`}
                  >
                    <input
                      type="checkbox"
                      checked={elegido}
                      disabled={esPrincipal}
                      onChange={() => toggle(sku)}
                      className="mt-0.5 h-4 w-4 shrink-0 accent-gold"
                    />
                    <Image
                      src={`/checkout/bump-${sku}.png`}
                      alt=""
                      width={56}
                      height={56}
                      loading="eager"
                      className="h-14 w-14 shrink-0 rounded-lg object-cover"
                    />
                    <span className="flex-1">
                      <span className="block text-sm font-semibold text-neutral-900">{p.title}</span>
                      <span className="mt-0.5 block text-xs text-neutral-500">{BUMP_DESCRIPTION[sku]}</span>
                      <span className="mt-1 flex items-center gap-2 text-xs">
                        <span className="text-neutral-400 line-through">{formatMoney(p.compareAt)}</span>
                        <span className="font-semibold text-emerald-700">{formatMoney(p.price)}</span>
                      </span>
                    </span>
                  </label>
                );
              })}
            </div>

            <div className="grid gap-4 md:sticky md:top-20 md:self-start">
              <div className="grid gap-2 rounded-xl border border-black/10 bg-neutral-50 p-4">
                {[...elegidos].map((sku) => (
                  <div key={sku} className="flex justify-between gap-4 text-sm">
                    <span className="text-neutral-500">{product(sku).title}</span>
                    <span className="text-neutral-900">{formatMoney(product(sku).price)}</span>
                  </div>
                ))}
                <div className="mt-1 flex items-end justify-between gap-4 border-t border-black/10 pt-2">
                  <span className="text-sm text-neutral-500">Total</span>
                  <span className="text-lg font-bold text-neutral-900">{formatMoney(total)}</span>
                </div>
              </div>

              {estado.paso === "error" && (
                <p role="alert" className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">
                  {estado.mensaje}
                </p>
              )}

              {country.gateway === "xpag" ? (
                <div className="grid gap-2">
                  <button
                    type="button"
                    disabled={estado.paso === "enviando"}
                    onClick={() => pagar("spei")}
                    className="btn-gold w-full"
                  >
                    {estado.paso === "enviando" ? "Procesando…" : `Pagar por SPEI · ${formatMoney(total)}`}
                  </button>
                  <button
                    type="button"
                    disabled={estado.paso === "enviando"}
                    onClick={() => pagar("oxxo")}
                    className="rounded-lg border border-black/15 px-4 py-2.5 text-sm font-semibold text-neutral-700 transition hover:border-black/30"
                  >
                    Pagar en efectivo (OXXO)
                  </button>
                </div>
              ) : (
                <button
                  type="button"
                  disabled={estado.paso === "enviando" || estado.paso === "redirigiendo"}
                  onClick={() => pagar()}
                  className="btn-gold w-full"
                >
                  {estado.paso === "enviando" || estado.paso === "redirigiendo"
                    ? "Abriendo el pago…"
                    : `Pagar ${formatMoney(total)}`}
                </button>
              )}

              <Link href="/panel" className="text-center text-sm text-neutral-400 underline">
                ← Volver a tu área
              </Link>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
