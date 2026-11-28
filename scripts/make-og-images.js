// make-og-images.js — Tao anh chia se OG 1200x630 (JPG, toi da 300 KB) cho
// moi truyen + anh mac dinh moi ngon ngu. Chay SAU eleventy trong
// `npm run build` (truoc strip-admin-config). Doc front matter bang js-yaml
// (co san qua eleventy), loc bai da dang giong isPublished trong
// eleventy.config.js (khong nhap, khong hen gio). Anh lay tu cover goc tren
// dia (src/media/...), cat giua (fit cover) ve 1200x630 bang sharp (co san
// qua @11ty/eleventy-img). Anh mac dinh: SVG (mau chu dao + ten web +
// tagline) -> JPEG. Truyen khong co cover dung anh mac dinh (template
// base.njk tu chon theo cover). (Dot 1 admin/chia-se, Ruler 10:00 28/11.)
const fs = require("fs");
const path = require("path");
const yaml = require("js-yaml");
const sharp = require("sharp");

const SITE_DIR = path.join(__dirname, "..");
const OUT_DIR = path.join(SITE_DIR, "_site", "img", "og");
const MAX_BYTES = 300 * 1024;
const W = 1200;
const H = 630;

const settings = JSON.parse(
  fs.readFileSync(path.join(SITE_DIR, "src", "_data", "settings.json"), "utf8")
);

function isPublished(data) {
  if (!data || data.draft === true) return false;
  const d = data.date ? new Date(data.date) : null;
  if (d && d > new Date()) return false; // bai hen gio: chi len khi rebuild sau ngay dang
  return true;
}

function resolveCover(raw) {
  if (!raw) return null;
  let p = String(raw).trim();
  if (p.startsWith("/media/")) p = "src" + p; // Sveltia ghi dang /media/...
  return path.join(SITE_DIR, p);
}

function esc(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

// Ngat tagline thanh toi da 2 dong, moi dong <= max ky tu (ngat theo tu).
function wrap(text, max) {
  const words = String(text).split(/\s+/).filter(Boolean);
  const lines = [];
  let cur = "";
  for (const w of words) {
    if (cur && (cur + " " + w).length > max) {
      lines.push(cur);
      cur = w;
    } else {
      cur = cur ? cur + " " + w : w;
    }
  }
  if (cur) lines.push(cur);
  return lines.slice(0, 2);
}

function defaultSvg(siteName, tagline) {
  const lines = wrap(tagline, 62);
  const tagLines = lines
    .map(
      (ln, i) =>
        `<text x="600" y="${352 + i * 44}" font-family="Georgia, 'Times New Roman', serif" font-size="30" fill="#d8dee8" text-anchor="middle">${esc(ln)}</text>`
    )
    .join("\n  ");
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <rect width="1200" height="630" fill="#1e3a5f"/>
  <rect x="480" y="302" width="240" height="4" fill="#b7791f"/>
  <text x="600" y="256" font-family="Georgia, 'Times New Roman', serif" font-size="64" fill="#fdfcf9" text-anchor="middle">${esc(siteName)}</text>
  ${tagLines}
</svg>`;
}

async function toJpeg(input, outPath, label) {
  // Cat giua ve 1200x630; giam quality dan neu vuot 300 KB.
  let q = 82;
  for (;;) {
    const buf = await sharp(input)
      .resize(W, H, { fit: "cover", position: "centre" })
      .jpeg({ quality: q, mozjpeg: true })
      .toBuffer();
    if (buf.length <= MAX_BYTES || q <= 55) {
      fs.writeFileSync(outPath, buf);
      console.log(
        `og: ${label} -> ${path.basename(outPath)} (${(buf.length / 1024).toFixed(0)} KB, q${q})`
      );
      return buf.length;
    }
    q -= 10;
  }
}

(async () => {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  // Anh mac dinh moi ngon ngu (dung khi truyen khong co cover + trang chu/chuyen muc).
  for (const lang of ["de", "pl"]) {
    const svg = defaultSvg(settings[`site_name_${lang}`], settings[`tagline_${lang}`]);
    await toJpeg(Buffer.from(svg), path.join(OUT_DIR, `default-${lang}.jpg`), `mac dinh ${lang}`);
  }
  let n = 0;
  const noCover = [];
  for (const lang of ["de", "pl"]) {
    const dir = path.join(SITE_DIR, "src", lang, "posts");
    if (!fs.existsSync(dir)) continue;
    for (const f of fs.readdirSync(dir).filter((x) => x.endsWith(".md")).sort()) {
      const raw = fs.readFileSync(path.join(dir, f), "utf8");
      const m = raw.match(/^---\n([\s\S]*?)\n---/);
      if (!m) {
        console.log(`og: CANH BAO ${lang}/${f} khong co front matter — bo qua`);
        continue;
      }
      const data = yaml.load(m[1]) || {};
      if (!isPublished(data)) continue;
      const slug = data.slug || f.replace(/\.md$/, "");
      const disk = resolveCover(data.cover);
      if (!disk || !fs.existsSync(disk)) {
        noCover.push(slug);
        console.log(`og: ${slug} khong co cover — dung anh mac dinh`);
        continue;
      }
      await toJpeg(disk, path.join(OUT_DIR, `${slug}.jpg`), slug);
      n++;
    }
  }
  console.log(`og: xong — ${n} anh truyen + 2 anh mac dinh trong ${OUT_DIR}`);
  if (noCover.length) console.log(`og: ${noCover.length} truyen khong cover: ${noCover.join(", ")}`);
})().catch((e) => {
  console.error("og: LOI", e);
  process.exit(1);
});
