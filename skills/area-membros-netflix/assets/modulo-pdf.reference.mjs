// PDF do módulo montado na hora a partir do MESMO array `pages` que o leitor usa
// (const MODULES no painel/index*.html). Não existe PDF separado para ficar velho:
// entrou página no leitor, entrou no PDF. Cache em memória pela assinatura
// (lista de páginas + tamanho/mtime de cada imagem).
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import crypto from 'node:crypto';

const PAGE_RE = /^conteudo(?:-es)?\/[a-z0-9-]+\/[\w.-]+\.jpe?g$/i;
const modulesCache = new Map(); // htmlPath -> { mtimeMs, mods }
const pdfCache = new Map(); // key -> { sig, buf, etag }

function readModules(htmlPath) {
  const st = fs.statSync(htmlPath);
  const hit = modulesCache.get(htmlPath);
  if (hit && hit.mtimeMs === st.mtimeMs) return hit.mods;
  const html = fs.readFileSync(htmlPath, 'utf8');
  const m = /const\s+MODULES\s*=\s*(\[[\s\S]*?\n\s*\]);/.exec(html);
  let mods = {};
  if (m) {
    const arr = vm.runInNewContext(m[1], {}, { timeout: 500 });
    for (const x of arr) if (x && x.sku && Array.isArray(x.pages)) mods[x.sku] = { title: String(x.title || x.sku), pages: x.pages.slice() };
  }
  modulesCache.set(htmlPath, { mtimeMs: st.mtimeMs, mods });
  return mods;
}

// Largura, altura e componentes de cor do JPEG (marcador SOF).
function jpegInfo(buf) {
  if (buf[0] !== 0xff || buf[1] !== 0xd8) return null;
  let i = 2;
  while (i + 9 < buf.length) {
    if (buf[i] !== 0xff) { i++; continue; }
    const mk = buf[i + 1];
    if (mk === 0xd8 || mk === 0x01 || (mk >= 0xd0 && mk <= 0xd7)) { i += 2; continue; }
    const len = buf.readUInt16BE(i + 2);
    if (mk >= 0xc0 && mk <= 0xcf && mk !== 0xc4 && mk !== 0xc8 && mk !== 0xcc) {
      return { h: buf.readUInt16BE(i + 5), w: buf.readUInt16BE(i + 7), comps: buf[i + 9] };
    }
    i += 2 + len;
  }
  return null;
}

// PDF mínimo: 1 imagem JPEG por página (DCTDecode, sem recompressão), largura A4.
function buildPdf(images) {
  const parts = [];
  const offsets = [];
  let size = 0;
  const push = (b) => { const x = typeof b === 'string' ? Buffer.from(b, 'latin1') : b; parts.push(x); size += x.length; };
  const obj = (n, body) => { offsets[n] = size; push(`${n} 0 obj\n`); for (const b of body) push(b); push('\nendobj\n'); };
  push('%PDF-1.4\n%\xe2\xe3\xcf\xd3\n');
  const n = images.length;
  const kids = images.map((_, k) => `${3 + k * 3 + 2} 0 R`).join(' ');
  obj(1, ['<< /Type /Catalog /Pages 2 0 R >>']);
  obj(2, [`<< /Type /Pages /Count ${n} /Kids [${kids}] >>`]);
  images.forEach(({ buf, w, h, comps }, k) => {
    const img = 3 + k * 3, content = img + 1, page = img + 2;
    const cs = comps === 1 ? '/DeviceGray' : comps === 4 ? '/DeviceCMYK /Decode [1 0 1 0 1 0 1 0]' : '/DeviceRGB';
    obj(img, [`<< /Type /XObject /Subtype /Image /Width ${w} /Height ${h} /ColorSpace ${cs} /BitsPerComponent 8 /Filter /DCTDecode /Length ${buf.length} >>\nstream\n`, buf, '\nendstream']);
    const pw = 595.28, ph = +(pw * h / w).toFixed(2);
    const draw = `q ${pw} 0 0 ${ph} 0 0 cm /Im0 Do Q`;
    obj(content, [`<< /Length ${draw.length} >>\nstream\n${draw}\nendstream`]);
    obj(page, [`<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ${pw} ${ph}] /Resources << /XObject << /Im0 ${img} 0 R >> >> /Contents ${content} 0 R >>`]);
  });
  const total = 3 + n * 3;
  const xref = size;
  push(`xref\n0 ${total}\n0000000000 65535 f \n`);
  for (let k = 1; k < total; k++) push(String(offsets[k]).padStart(10, '0') + ' 00000 n \n');
  push(`trailer\n<< /Size ${total} /Root 1 0 R >>\nstartxref\n${xref}\n%%EOF\n`);
  return Buffer.concat(parts, size);
}

// Devolve { buf, etag, title } do módulo, ou null quando o módulo não tem páginas
// próprias válidas (aí o servidor cai no PDF estático antigo).
export function modulePdf(root, sku, lang) {
  const painel = path.join(root, 'painel');
  const htmlPath = path.join(painel, lang === 'es' ? 'index-es.html' : 'index.html');
  const mod = readModules(htmlPath)[sku];
  const pages = mod && mod.pages;
  if (!pages || !pages.length || !pages.every((p) => PAGE_RE.test(p))) return null;
  const files = pages.map((p) => path.join(painel, p));
  const stats = [];
  for (const f of files) {
    try { stats.push(fs.statSync(f)); } catch { return null; }
  }
  const sig = mod.title + '|' + files.map((f, k) => `${f}:${stats[k].size}:${stats[k].mtimeMs}`).join('|');
  const key = `${lang || 'pt'}:${sku}`;
  const hit = pdfCache.get(key);
  if (hit && hit.sig === sig) return hit;
  const images = [];
  for (const f of files) {
    const buf = fs.readFileSync(f);
    const info = jpegInfo(buf);
    if (!info) return null;
    images.push({ buf, ...info });
  }
  const buf = buildPdf(images);
  const etag = '"' + crypto.createHash('sha1').update(sig).digest('hex').slice(0, 20) + '"';
  const out = { sig, buf, etag, title: mod.title };
  pdfCache.set(key, out);
  return out;
}
