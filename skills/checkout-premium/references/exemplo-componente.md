# Exemplo de componente completo

Este é o componente que originou a skill (`CheckoutHotmartTeste.tsx`, projeto
"El Número Maestro"), como ponto de partida pra copiar e adaptar — não copie
literal: troque cores, textos, lib de pricing/country/cart pelas do projeto
atual, e ajuste a seção de pagamento pro gateway certo (ver tabela no
SKILL.md).

O que muda de projeto pra projeto, sempre:
- `PRODUCT_TITLE`, `price()`, `comparePrice()`, `BUMP_SKUS`, `product()` — vêm
  da lib de pricing do projeto atual, nunca hardcode um número.
- `isMx` / country check — troque pela lib de país/gateway do projeto atual.
- `addSku`/`removeSku` — lib de carrinho do projeto atual, se existir; se não
  existir, o toggle do bump pode ficar só em estado local do componente.
- `CheckoutExitOffer` — só importe se o projeto já tiver um componente assim;
  se não tiver, pergunte ao usuário antes de escrever um novo do zero.
- `/api/lead-email` — endpoint que persiste o email cedo (ver corpo abaixo);
  crie um equivalente se o projeto não tiver, usando a lib de lead/db dele.
- Fotos de depoimento e cor de marca (`--color-gold-deep` etc.) — trocar
  pelos assets e paleta reais do projeto.
- `RESENAS_MX`/`RESENAS_AR` — o padrão de "um set por mercado" só se aplica
  se o projeto atender mais de um país; um projeto de mercado único usa um
  set só.

```tsx
"use client";

import { useCallback, useEffect, useState } from "react";
import Image from "next/image";
import {
  PRODUCT_TITLE,
  product,
  formatMoney,
  price,
  comparePrice,
  BUMP_SKUS,
} from "@/lib/pricing";
import { isMx } from "@/lib/country";
import { addSku, removeSku } from "@/lib/cart";
import CheckoutExitOffer from "@/components/CheckoutExitOffer";

interface StoredLead {
  leadId: string;
  name?: string;
  email?: string;
}

const DURACION_S = 15 * 60;

function useCuentaRegresiva(segundos: number) {
  const [restante, setRestante] = useState(segundos);
  useEffect(() => {
    const id = setInterval(() => setRestante((r) => (r > 0 ? r - 1 : 0)), 1000);
    return () => clearInterval(id);
  }, []);
  const min = String(Math.floor(restante / 60)).padStart(2, "0");
  const seg = String(restante % 60).padStart(2, "0");
  return `${min}:${seg}`;
}

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

// Un set de reseñas por mercado — fotos/nombres reales de la lib de
// testimonios del proyecto, nunca "Cliente Ejemplo".
const RESENAS_MX = [
  {
    nombre: "Silvia M.",
    foto: "/testimonios/mx-1.jpg",
    estrellas: 5,
    texto: "No creía nada cuando lo compré, pero funcionó...",
  },
  // ...resto del set, 3-4 entradas, estrellas variando entre 4 y 5
];

// Nombres/ciudades del toast de compra — variados, sin dato real de nadie.
const NOMBRES_TOAST = ["María G.", "Carlos R.", "Ana L.", "José M.", "Sofía T."];
const CIUDADES_TOAST = ["Ciudad de México", "Guadalajara", "Monterrey"];

function useToastCompra() {
  const [visible, setVisible] = useState(false);
  const [idx, setIdx] = useState(0);

  useEffect(() => {
    let mostrar: ReturnType<typeof setTimeout>;
    let ocultar: ReturnType<typeof setTimeout>;
    const ciclo = (retraso: number) => {
      mostrar = setTimeout(() => {
        setIdx((i) => (i + 1) % NOMBRES_TOAST.length);
        setVisible(true);
        ocultar = setTimeout(() => {
          setVisible(false);
          ciclo(9000 + Math.random() * 6000);
        }, 5000);
      }, retraso);
    };
    ciclo(4000);
    return () => {
      clearTimeout(mostrar);
      clearTimeout(ocultar);
    };
  }, []);

  return { visible, nombre: NOMBRES_TOAST[idx], ciudad: CIUDADES_TOAST[idx % CIUDADES_TOAST.length] };
}

type MetodoMx = "spei" | "oxxo";
type MetodoAr = "mercadopago" | "transferencia";

export default function CheckoutHotmartStyle() {
  const [email, setEmail] = useState("");
  const [metodoMx, setMetodoMx] = useState<MetodoMx>("spei");
  const [metodoAr, setMetodoAr] = useState<MetodoAr>("mercadopago");
  const [bumps, setBumps] = useState<Set<string>>(() => new Set(BUMP_SKUS)); // pré-marcado
  const [erro, setErro] = useState<string | null>(null);
  const [enviando, setEnviando] = useState(false);
  const [arte, setArte] = useState(true);
  const [leadId, setLeadId] = useState<string | null>(null);
  const [emailGuardado, setEmailGuardado] = useState(false);
  // Número não-redondo, fixado uma vez por sessão.
  const [clientesCount] = useState(() => 700 + Math.floor(Math.random() * 180));

  const valorBase = price();
  const antesBase = comparePrice();
  const tiempo = useCuentaRegresiva(DURACION_S);
  const toast = useToastCompra();

  useEffect(() => {
    try {
      const raw = localStorage.getItem("lc_lead");
      const lead = raw ? (JSON.parse(raw) as StoredLead) : null;
      if (lead?.leadId) setLeadId(lead.leadId);
      if (lead?.email && EMAIL_RE.test(lead.email)) setEmail(lead.email);
    } catch {
      // sin lead: el form sigue funcionando, solo no captura para remarketing.
    }
  }, []);

  const bumpProducts = BUMP_SKUS.map((sku) => product(sku));
  const valor = valorBase + bumpProducts.reduce((acc, p) => (bumps.has(p.sku) ? acc + p.price : acc), 0);
  const antes = antesBase + bumpProducts.reduce((acc, p) => (bumps.has(p.sku) ? acc + p.compareAt : acc), 0);

  const toggleBump = (sku: string) => {
    setBumps((prev) => {
      const next = new Set(prev);
      if (next.has(sku)) {
        next.delete(sku);
        removeSku(sku as any);
      } else {
        next.add(sku);
        addSku(sku as any);
      }
      return next;
    });
  };

  // Captura el email ANTES del clic en comprar — ver SKILL.md #4.
  const guardarEmailTemprano = useCallback(() => {
    const limpio = email.trim().toLowerCase();
    if (!EMAIL_RE.test(limpio) || !leadId || emailGuardado) return;
    setEmailGuardado(true);
    try {
      const raw = localStorage.getItem("lc_lead");
      const lead = raw ? (JSON.parse(raw) as StoredLead) : null;
      if (lead) localStorage.setItem("lc_lead", JSON.stringify({ ...lead, email: limpio }));
    } catch {}
    fetch("/api/lead-email", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ leadId, email: limpio }),
    }).catch(() => setEmailGuardado(false));
  }, [email, leadId, emailGuardado]);

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    const limpio = email.trim().toLowerCase();
    if (!EMAIL_RE.test(limpio)) {
      setErro("Escribe un correo válido.");
      return;
    }
    setErro(null);
    guardarEmailTemprano();
    setEnviando(true);
    // chamar API real de checkout aqui
  };

  return (
    <main className="checkout-page min-h-dvh">
      {/* 1. Barra de urgencia full-bleed */}
      <div
        className="sticky top-0 z-10 flex w-full items-center justify-center gap-3 px-4 py-3 text-center text-white"
        style={{
          background: "linear-gradient(180deg, #E8544C 0%, #D6382F 100%)",
          boxShadow: "0 10px 25px -12px rgba(214, 56, 47, 0.65), inset 0 -1px 0 rgba(0,0,0,0.15)",
        }}
      >
        <span className="font-mono text-lg font-bold tabular-nums drop-shadow-sm">{tiempo}</span>
        <span className="flex items-center gap-1.5 text-sm font-medium">
          {/* Ícono de reloj real — círculo + un puntero, no lupa/ampolheta */}
          <svg viewBox="0 0 20 20" className="h-4 w-4 shrink-0" fill="none" aria-hidden>
            <circle cx="10" cy="10" r="7.5" stroke="currentColor" strokeWidth="1.4" />
            <path d="M10 6v4.2l2.8 1.8" stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
          ¡Aprovecha esta oferta!
        </span>
      </div>

      <div className="mx-auto w-full max-w-3xl px-4 py-6 sm:py-10">
        {/* 2. Banner — <Image fill>, NO el componente de banner del proyecto si tiene ancho fijo */}
        <div className="relative aspect-[1672/941] w-full overflow-hidden rounded-t-2xl border border-b-0 border-gold/25 bg-neutral-900">
          {arte && (
            <Image
              src="/checkout/banner-desktop.jpg"
              alt=""
              fill
              priority
              sizes="(min-width: 768px) 768px, 100vw"
              className="object-cover"
              onError={() => setArte(false)}
            />
          )}
        </div>

        <section className="rounded-b-2xl border border-t-0 border-gold/25 bg-white p-5 shadow-[0_20px_45px_-30px_rgba(42,22,8,0.35)] sm:p-8 md:p-10">
          {/* 3. Header: nombre en color de marca (NUNCA negro puro), precio, sello de garantía */}
          <div className="mb-6 flex items-center justify-between gap-4 border-b border-black/10 pb-5">
            <div>
              <p className="text-lg font-bold sm:text-xl" style={{ color: "var(--color-brand-deep)" }}>
                {PRODUCT_TITLE}
              </p>
              <p className="text-sm text-neutral-500">Pago único · Acceso de por vida</p>
              <span className="mt-2 inline-flex items-center gap-1.5 rounded-full border border-emerald-200 bg-emerald-50 px-2.5 py-1 text-[11px] font-semibold text-emerald-700">
                Garantía de 7 días
              </span>
            </div>
            <div className="text-right">
              {antes > valor && <p className="text-sm text-neutral-400 line-through">{formatMoney(antes)}</p>}
              <p className="text-xl font-bold text-neutral-900 sm:text-2xl">{formatMoney(valor)}</p>
            </div>
          </div>

          <form onSubmit={submit} className="grid gap-6 md:grid-cols-[minmax(0,1fr)_20rem] md:items-start md:gap-8">
            <div className="grid gap-6">
              {/* 4. Formulario mínimo — solo email */}
              <div className="grid gap-1.5">
                <label htmlFor="email" className="text-sm font-medium text-neutral-900">Tu email</label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  onBlur={guardarEmailTemprano}
                  placeholder="tucorreo@ejemplo.com"
                  className="min-h-[48px] rounded-lg border border-black/15 bg-white px-4 text-base text-neutral-900 outline-none focus:border-gold"
                />
                {erro && <p role="alert" className="text-sm text-red-600">{erro}</p>}
              </div>

              {/* 5. Order bump — checkbox pré-marcado, foto real, copy validado contra o produto real */}
              {bumpProducts.length > 0 && (
                <div className="grid gap-2">
                  <p className="text-sm font-medium text-neutral-900">Aprovecha y suma:</p>
                  {bumpProducts.map((p) => (
                    <label
                      key={p.sku}
                      className={`flex cursor-pointer items-start gap-3 rounded-xl border p-3.5 transition ${
                        bumps.has(p.sku) ? "border-gold bg-gold/10" : "border-emerald-200 bg-emerald-50/50 hover:border-emerald-300"
                      }`}
                    >
                      <input type="checkbox" checked={bumps.has(p.sku)} onChange={() => toggleBump(p.sku)} className="mt-0.5 h-4 w-4 shrink-0 accent-gold" />
                      <Image src="/checkout/bump-foto.png" alt="" width={56} height={56} loading="eager" className="h-14 w-14 shrink-0 rounded-lg object-cover" />
                      <span className="flex-1">
                        <span className="block text-sm font-semibold text-neutral-900">{p.title}</span>
                        <span className="mt-0.5 block text-xs text-neutral-500">{/* copy real, puxado de outro componente */}</span>
                        <span className="mt-1 flex items-center gap-2 text-xs">
                          <span className="text-neutral-400 line-through">{formatMoney(p.compareAt)}</span>
                          <span className="font-semibold text-emerald-700">{formatMoney(p.price)}</span>
                        </span>
                      </span>
                    </label>
                  ))}
                </div>
              )}

              {/* 6. Pagamento — condicional ao gateway, ver tabela do SKILL.md */}
              <div className="grid gap-1.5">
                <p className="text-sm font-medium text-neutral-900">Forma de pago</p>
                {isMx ? (
                  <div className="grid grid-cols-2 gap-3">
                    {/* botão SPEI, botão OXXO — mesmo padrão do bloco de baixo */}
                  </div>
                ) : (
                  <div className="grid grid-cols-2 gap-3">
                    {/* botão Tarjeta (Mercado Pago), botão Transferencia manual */}
                  </div>
                )}
              </div>
            </div>

            {/* 7. Resumo + CTA — coluna sticky no desktop */}
            <div className="grid gap-4 md:sticky md:top-20 md:self-start">
              <div className="grid gap-2 rounded-xl border border-black/10 bg-neutral-50 p-4">
                <div className="flex justify-between gap-4 text-sm">
                  <span className="text-neutral-500">{PRODUCT_TITLE}</span>
                  <span className="text-neutral-900">{formatMoney(valorBase)}</span>
                </div>
                {bumpProducts.filter((p) => bumps.has(p.sku)).map((p) => (
                  <div key={p.sku} className="flex justify-between gap-4 text-sm">
                    <span className="text-neutral-500">{p.title}</span>
                    <span className="text-neutral-900">{formatMoney(p.price)}</span>
                  </div>
                ))}
                <div className="mt-1 flex items-end justify-between gap-4 border-t border-black/10 pt-2">
                  <span className="text-sm text-neutral-500">Total</span>
                  <span className="text-lg font-bold text-neutral-900">{formatMoney(valor)}</span>
                </div>
              </div>
              <button type="submit" disabled={enviando} className="btn-gold min-h-[50px] rounded-lg text-base font-semibold disabled:opacity-60">
                {enviando ? "Generando…" : "Comprar ahora"}
              </button>
              <p className="text-center text-[11px] text-neutral-400">Protegido · Pago 100% seguro</p>
            </div>
          </form>

          {/* 8. Prueba social — fotos/nombres reales, estrellas 4-5, contador no redondo */}
          <div className="mt-8 border-t border-black/10 pt-6">
            <p className="mb-3 text-sm font-semibold text-neutral-900">{clientesCount} clientes ya compraron</p>
            <div className="grid gap-4 sm:grid-cols-2">
              {RESENAS_MX.map((r) => (
                <div key={r.nombre} className="flex items-start gap-2.5">
                  {/* <img> normal si los assets tienen extensión/content-type que no coincide — ver SKILL.md #1 */}
                  <img src={r.foto} alt="" className="h-9 w-9 shrink-0 rounded-full object-cover" />
                  <div className="min-w-0">
                    <p className="flex items-center gap-1.5 text-sm font-medium text-neutral-900">
                      {r.nombre}
                      <span className="text-amber-500" aria-hidden>
                        {"★".repeat(r.estrellas)}
                        <span className="text-neutral-300">{"★".repeat(5 - r.estrellas)}</span>
                      </span>
                    </p>
                    <p className="mt-0.5 text-xs leading-relaxed text-neutral-500">{r.texto}</p>
                  </div>
                </div>
              ))}
            </div>
            {/* 11. Sellos de confianza */}
            <p className="mt-6 text-center text-xs text-neutral-400">
              Tus datos están protegidos con criptografía y conformidad PCI DSS durante todo el proceso.
            </p>
          </div>
        </section>
      </div>

      {/* 10. Popup de saída — reusar componente existente do projeto */}
      {leadId && <CheckoutExitOffer armed leadId={leadId} onAceptar={() => {}} />}

      {/* 9. Notificación fake de compra — canto superior direito, ciclos de 10-15s */}
      <div
        role="status"
        aria-live="polite"
        className={`fixed right-4 top-20 z-20 flex max-w-[280px] items-center gap-3 rounded-xl border border-black/10 bg-white p-3 shadow-[0_15px_35px_-10px_rgba(0,0,0,0.25)] transition-all duration-500 ${
          toast.visible ? "translate-y-0 opacity-100" : "pointer-events-none -translate-y-3 opacity-0"
        }`}
      >
        <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full text-sm font-bold text-white" style={{ background: "linear-gradient(135deg, #E8A31E, #B26A00)" }} aria-hidden>
          {toast.nombre.charAt(0)}
        </span>
        <div className="min-w-0">
          <p className="truncate text-sm font-semibold text-neutral-900">{toast.nombre}</p>
          <p className="truncate text-xs text-neutral-500">acaba de comprar · {toast.ciudad}</p>
        </div>
      </div>
    </main>
  );
}
```

## Endpoint de captura de email cedo (`/api/lead-email`)

Rota nova que persiste o email associado a um lead assim que ele digita
(`onBlur`), não só no submit final. Adapte à lib de lead/db do projeto atual:

```ts
import { NextResponse } from "next/server";
import { getLead, updateLead } from "@/lib/db";

export const runtime = "nodejs";
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

export async function POST(request: Request) {
  const body = (await request.json().catch(() => null)) as Record<string, unknown> | null;
  if (!body) return NextResponse.json({ error: "Cuerpo inválido." }, { status: 400 });

  const leadId = String(body.leadId ?? "").trim();
  const email = String(body.email ?? "").trim().toLowerCase();
  if (!EMAIL_RE.test(email)) return NextResponse.json({ error: "Email inválido." }, { status: 400 });

  const lead = await getLead(leadId);
  if (!lead) return NextResponse.json({ ok: true, ignored: "lead inexistente" });

  await updateLead(leadId, { email });
  return NextResponse.json({ ok: true });
}
```
