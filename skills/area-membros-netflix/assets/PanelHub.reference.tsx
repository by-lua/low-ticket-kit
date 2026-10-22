"use client";

import { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { firstName } from "@/lib/numerology";
import { BUMP_SKUS, BUMP_DESCRIPTION, BUMP_PUNTOS, BUMP_CATEGORIA, product, formatMoney, type Sku } from "@/lib/pricing";
import { t } from "@/lib/copy";
import Modal from "@/components/Modal";

const SOPORTE_EMAIL = "voce@exemplo.com";

interface Props {
  nombre: string;
  /** SKUs de todas las órdenes aprobadas de esta persona (unión, sin duplicados). */
  skusComprados: string[];
}

interface Modulo {
  sku: Sku;
  /** Etiqueta corta arriba del título, tipo "EL CUARTO NÚMERO" en la lectura del núcleo. */
  categoria: string;
  title: string;
  subtitle: string;
  image: string;
  /** A dónde manda cuando YA está desbloqueado. */
  href: string;
  /** El núcleo siempre está desbloqueado — es lo que ella ya vino a buscar. */
  siempreDesbloqueado?: boolean;
}

const MODULOS: Modulo[] = [
  {
    sku: "core",
    categoria: "EL NÚCLEO",
    title: "Tu Número Maestro",
    subtitle: "La lectura completa",
    image: "/oferta/mockup-producto.png",
    href: "/panel/lectura",
    siempreDesbloqueado: true,
  },
  {
    sku: "apellido",
    categoria: BUMP_CATEGORIA.apellido ?? "",
    title: product("apellido").title,
    subtitle: BUMP_DESCRIPTION.apellido ?? "",
    image: "/checkout/bump-apellido.png",
    // Antes esto también mandaba a /soporte: la lectura del apellido ya vive
    // en el PDF que se manda por email, pero acá adentro no tenía página
    // propia. Con /panel/apellido, quien ya lo pagó ve el contenido en el
    // momento en vez de tener que ir a buscar el mail.
    href: "/panel/apellido",
  },
  ...BUMP_SKUS.filter((s) => s !== "apellido").map((sku) => ({
    sku,
    categoria: BUMP_CATEGORIA[sku] ?? "",
    title: product(sku).title,
    subtitle: BUMP_DESCRIPTION[sku] ?? "",
    image: `/checkout/bump-${sku}.png`,
    // "Tu Año Personal" y "El Audio de tu Ángel Numérico" ya tienen
    // contenido propio (cálculo del año / audio grabado) y página en el
    // panel — misma lógica que "apellido" arriba.
    href: sku === "anio" ? "/panel/anio" : "/panel/audio-angel",
  })),
];

/**
 * Área de miembros estilo Netflix, con la MISMA paleta clara y dorada del
 * resto del sitio (`--color-night` #FFFCF6, decisión 2026-09-06) — no un
 * negro/morado inventado aparte. Un módulo por producto, el que ya compró
 * desbloqueado y a color, el que no en gris con candado — clic abre un modal
 * con explicación breve y el precio, no la deja mandada a otra pantalla sin
 * contexto.
 *
 * El CTA de "comprar" en ese modal manda a /soporte y no a un checkout propio
 * de re-compra: agregar un módulo después de la venta principal dispara la
 * MISMA maquinaria de aprobación que el núcleo (deliverAt, email de
 * confirmación, Purchase de la CAPI con el valor completo), y esa maquinaria
 * da por hecho que toda orden aprobada entrega la lectura completa. Sin
 * adaptarla primero, vender el add-on por acá reenviaría el PDF entero como
 * si fuera una compra nueva del núcleo. La venta post-compra sigue el canal
 * que YA existe (carga manual en /admin, `source: "whatsapp"`), no uno nuevo
 * sin esa guarda.
 */
export default function PanelHub({ nombre, skusComprados }: Props) {
  const comprados = new Set(skusComprados);
  const primero = firstName(nombre);
  const router = useRouter();
  const [modalSku, setModalSku] = useState<Sku | null>(null);
  const modulo = modalSku ? MODULOS.find((m) => m.sku === modalSku) : undefined;

  async function salir() {
    await fetch("/api/session", { method: "DELETE" });
    router.push("/entrar");
  }

  /*
   * SIN "aura grain" acá: esas clases son el fondo decorativo FIJO
   * (`position:fixed; z-index:-2`) que `layout.tsx` ya pinta UNA vez para
   * todo el sitio (`<div className="aura" />`, fuera de este árbol).
   * Ponerlas también en este contenedor de contenido real metía TODA la
   * página — hero, cards, todo — en ese mismo `position:fixed` con
   * z-index negativo: se veía perfecto, pero ningún click llegaba a nada
   * (`elementFromPoint` devolvía `<body>` en el lugar de cada card). Fue
   * el motivo real de "hago clic y no pasa nada" reportado en producción.
   */
  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      {/*
       * Hero con imagen de fondo a todo el ancho, que se desvanece hacia el
       * fondo claro de la página — mismo patrón que el mockup de referencia
       * (imagen arriba, degradé, título flotando sobre el degradé, grid
       * abajo ya sobre fondo sólido). La barra superior (soporte/salir) va
       * ENCIMA de la imagen, en texto claro, porque acá abajo hay foto, no
       * el fondo crema del resto del sitio.
       */}
      {/*
       * Banner de altura FIJA, no aspect-ratio: la versión con título
       * flotando dentro del degradé (position:absolute anclado al fondo de
       * un contenedor con aspect-ratio) media mal en este layout — el
       * contenedor terminaba más alto de lo que se veía y el título quedaba
       * tapado por la grilla de abajo. Altura fija es más simple y no tiene
       * ese modo de falla: la imagen ocupa un bloque de tamaño conocido, el
       * título va DESPUÉS, en flujo normal, siempre visible.
       */}
      <div
        style={{
          position: "relative",
          height: "13rem",
          backgroundImage: "url(/panel-hero-bg.png)",
          backgroundSize: "cover",
          backgroundPosition: "center 35%",
        }}
      >
        {/* Barra superior, sobre la imagen. La imagen salió clara/luminosa a
            propósito (mismo tono crema del sitio), así que el texto encima
            es oscuro, no claro — un texto claro acá se funde y no se lee. */}
        <div
          style={{
            display: "flex",
            justifyContent: "flex-end",
            alignItems: "center",
            gap: "1.25rem",
            padding: "1rem 1.5rem",
            fontSize: "0.78rem",
          }}
        >
          <a
            href={`mailto:${SOPORTE_EMAIL}`}
            style={{ color: "var(--color-bone)", display: "inline-flex", alignItems: "center", gap: "0.35rem" }}
          >
            <span aria-hidden>✉️</span>
            {t("Soporte", "Soporte")}
          </a>
          <button
            type="button"
            onClick={salir}
            style={{
              color: "var(--color-bone)",
              background: "rgba(255,255,255,0.7)",
              border: "1px solid rgba(42,27,15,0.2)",
              borderRadius: "999px",
              padding: "0.4rem 0.9rem",
              cursor: "pointer",
              fontWeight: 600,
            }}
          >
            {t("Cerrar sesión", "Cerrar sesión")}
          </button>
        </div>

        {/* Degradé al pie, para que la imagen se funda con el fondo de la
            página en vez de cortar en seco. */}
        <div
          style={{
            position: "absolute",
            inset: 0,
            background: "linear-gradient(to bottom, transparent 60%, var(--color-night) 100%)",
          }}
        />
      </div>

      {/* Título — en flujo normal, DEBAJO del banner, nunca superpuesto. */}
      <div style={{ padding: "0.5rem 1.5rem 2.5rem", textAlign: "center" }}>
        <p className="eyebrow" style={{ marginBottom: "0.5rem" }}>
          {t("Bienvenida de nuevo", "Bienvenida de nuevo")}
        </p>
        <h1 className="display gold-text" style={{ fontSize: "clamp(1.8rem, 5vw, 2.75rem)" }}>
          {primero ? `${primero}, tu área` : "Tu área"}
        </h1>
      </div>

      {/*
       * Flexbox, no grid — `repeat(auto-fit, minmax(...))` con pocos ítems y
       * mucho ancho de sobra reparte el espacio sobrante de forma dispareja
       * entre columnas (hueco grande en el medio, cards pegadas a los
       * costados). Con flex-wrap + justify-content:center y cada card con
       * ancho fijo, el espacio sobrante va a los MÁRGENES afuera del grupo,
       * no entre las cards.
       */}
      {/*
       * Mobile: scroll horizontal (carrusel), como en la referencia — no
       * quiebra línea, la fila entera se desliza. Desktop (`sm:` en
       * adelante): vuelve al flex-wrap centrado de arriba.
       */}
      <div
        className="flex flex-nowrap overflow-x-auto sm:flex-wrap sm:overflow-visible snap-x snap-mandatory sm:snap-none justify-start sm:justify-center"
        style={{
          flex: 1,
          maxWidth: "70rem",
          width: "100%",
          margin: "0 auto",
          padding: "0 1.5rem 4rem",
          gap: "1.25rem",
        }}
      >
        {MODULOS.map((m) => {
          const desbloqueado = m.siempreDesbloqueado || comprados.has(m.sku);

          const tarjeta = (
            <div
              style={{
                borderRadius: "0.85rem",
                overflow: "hidden",
                border: desbloqueado
                  ? "1px solid rgba(232,163,30,0.35)"
                  : "1px solid rgba(42,27,15,0.12)",
                background: "#fff",
                boxShadow: desbloqueado
                  ? "0 4px 20px rgba(178,106,0,0.12)"
                  : "0 2px 8px rgba(42,27,15,0.06)",
                transition: "transform 0.15s ease, border-color 0.15s ease",
              }}
            >
              <div style={{ position: "relative", aspectRatio: "1 / 1", width: "100%" }}>
                <Image
                  src={m.image}
                  alt=""
                  fill
                  sizes="240px"
                  unoptimized
                  style={{
                    objectFit: "cover",
                    filter: desbloqueado ? "none" : "grayscale(1) opacity(0.55)",
                  }}
                />
                {!desbloqueado && (
                  <div
                    style={{
                      position: "absolute",
                      inset: 0,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      background: "rgba(255,255,255,0.15)",
                    }}
                  >
                    {/* Candado propio en vez del emoji — el emoji rompe el
                        tono "premium" del resto de la tarjeta. El precio NO
                        va acá: se ve recién al hacer clic, en el modal. */}
                    <span
                      aria-hidden
                      style={{
                        width: "2.75rem",
                        height: "2.75rem",
                        borderRadius: "50%",
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                        background: "rgba(255,255,255,0.85)",
                        boxShadow: "0 2px 10px rgba(42,27,15,0.25)",
                      }}
                    >
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <rect x="5" y="11" width="14" height="10" rx="2" stroke="var(--color-gold-deep)" strokeWidth="1.8" />
                        <path d="M8 11V7a4 4 0 0 1 8 0v4" stroke="var(--color-gold-deep)" strokeWidth="1.8" strokeLinecap="round" />
                        <circle cx="12" cy="16" r="1.6" fill="var(--color-gold-deep)" />
                      </svg>
                    </span>
                  </div>
                )}
              </div>
              <div style={{ padding: "0.75rem 0.85rem" }}>
                {/* Etiqueta de categoría — mismo patrón que "EL CUARTO NÚMERO"
                    arriba del título en la lectura del núcleo. Sin esto el
                    módulo se veía más pobre que la lectura principal. */}
                <p
                  className="eyebrow"
                  style={{ fontSize: "0.6rem", marginBottom: "0.3rem", opacity: desbloqueado ? 1 : 0.6 }}
                >
                  {m.categoria}
                </p>
                <p
                  style={{
                    fontSize: "0.9rem",
                    fontWeight: 600,
                    color: "var(--color-bone)",
                    opacity: desbloqueado ? 1 : 0.55,
                    marginBottom: "0.25rem",
                  }}
                >
                  {m.title}
                </p>
                {/* El subtítulo dice qué ES el módulo, comprado o no — "Todavía
                    no la desbloqueaste" no vende nada, un resumen sí. */}
                <p style={{ fontSize: "0.76rem", color: "var(--color-mist)", lineHeight: 1.35 }}>
                  {m.subtitle}
                </p>
              </div>
            </div>
          );

          // Desbloqueado: navega directo a su contenido. Bloqueado: abre el
          // modal con la explicación y el precio, en vez de mandarla a otra
          // pantalla sin haber visto qué es lo que está comprando.
          if (desbloqueado) {
            return (
              <Link
                key={m.sku}
                href={m.href}
                className="snap-start"
                style={{ display: "block", width: "220px", flexShrink: 0 }}
              >
                {tarjeta}
              </Link>
            );
          }
          return (
            <button
              key={m.sku}
              type="button"
              onClick={() => setModalSku(m.sku)}
              className="snap-start"
              style={{
                display: "block",
                width: "220px",
                flexShrink: 0,
                textAlign: "left",
                padding: 0,
                border: 0,
                background: "none",
                cursor: "pointer",
              }}
            >
              {tarjeta}
            </button>
          );
        })}
      </div>

      {/*
       * Modal del módulo bloqueado — mismo tono de venta que `BumpModal`
       * (el que ya vende "apellido" ANTES del checkout, con bullets y precio
       * tachado). Antes este modal era solo título+subtítulo+botón: mucho
       * más flojo que el bump que sí convierte en el checkout. Si vende ahí,
       * tiene que vender acá también — es la misma decisión de compra.
       */}
      <Modal open={!!modulo} title={modulo?.title ?? ""} onClose={() => setModalSku(null)}>
        {modulo && (
          <div className="space-y-5">
            <div className="space-y-3 text-center">
              <p className="eyebrow text-gold uppercase">
                {t("Todavía no lo tenés", "Todavía no lo tienes")}
              </p>
              <h2 className="display text-xl sm:text-2xl text-bone">{modulo.title}</h2>
              <p className="text-mist leading-relaxed">{modulo.subtitle}</p>
            </div>

            <div className="hairline" />

            <ul className="space-y-3 text-bone">
              {(BUMP_PUNTOS[modulo.sku] ?? []).map((punto, i) => (
                <li key={i} className="flex items-start gap-3">
                  <span className="text-gold text-xl leading-none mt-1" aria-hidden>
                    +
                  </span>
                  <span>{punto}</span>
                </li>
              ))}
            </ul>

            <div className="modal-actions space-y-3">
              <div className="flex items-center justify-center gap-2 text-sm">
                <span className="text-mist/60 line-through">
                  {formatMoney(product(modulo.sku as Exclude<Sku, "core">).compareAt)}
                </span>
                <span className="display text-2xl text-gold-soft">
                  {formatMoney(product(modulo.sku as Exclude<Sku, "core">).price)}
                </span>
              </div>
              <p className="text-center text-mist text-sm">
                {t(
                  "Se suma a lo que ya compraste, en un pago aparte.",
                  "Se suma a lo que ya compraste, en un pago aparte.",
                )}
              </p>
              <a
                href={`/panel/comprar/${modulo.sku}`}
                className="btn-gold w-full inline-flex items-center justify-center"
              >
                {`Lo quiero por ${formatMoney(product(modulo.sku as Exclude<Sku, "core">).price)}`}
              </a>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
}
