// strip-admin-config.js — Bo dong binh luan (#) khoi src/admin/config.yml
// khi build, de file config.yml trien khai chi chua cau hinh (Ruler 11:50
// 27/11: config.yml live lo ghi chu noi bo tieng Viet). Chay sau eleventy
// (passthrough da copy ban co chu thich vao _site/admin/), ghi de bang ban
// sach. Ban goc co chu thich o src/admin/config.yml GIU NGUYEN (nguon duy
// nhat, khong sua tay ban sach). Cong kiem muc 12 kiem lai tren _site.
//
// Loc admin theo ngon ngu (Phuong an A, Ruler 15:52 27/11): khi build voi
// SITE_LANG=de|pl, bo khoi ban build: collection truyen cua ngon ngu kia
// (posts_pl / posts_de) + muc file cua ngon ngu kia trong collection About
// (o_nas / ueber_uns) va Legal (polityka, kontakt / impressum, datenschutz,
// kontakt_de) + truong menu cua ngon ngu kia trong file menus.json
// (pl_header/pl_footer o ban de, de_header/de_footer o ban pl — Ruler
// 11:20 28/11: #07 live van con pl_header/pl_footer vi truoc day chua loc
// truong menu). Giu nguyen: Categories, Settings (file cau hinh chung),
// file menus (chi bo 2 truong cua ngon ngu kia) va cac collection
// About/Legal cua ngon ngu nay. Ban nguon GIU NGUYEN du 2 collection
// (chi loc ban build). Khong cham backend/auth/token.
const fs = require("fs");
const path = require("path");

const SITE_LANG = process.env.SITE_LANG || "";
if (SITE_LANG && SITE_LANG !== "de" && SITE_LANG !== "pl") {
  throw new Error(`SITE_LANG khong hop le: ${JSON.stringify(SITE_LANG)} (chi duoc "de" hoac "pl")`);
}
const OTHER = SITE_LANG === "de" ? "pl" : SITE_LANG === "pl" ? "de" : "";
// Collection truyen cua ngon ngu kia (bo ca khoi) + muc file cua ngon ngu kia.
const DROP_COLLECTION = OTHER ? [`posts_${OTHER}`] : [];
const DROP_FILE = {
  // collection -> tap muc file cua ngon ngu kia
  about: OTHER === "pl" ? ["o_nas"] : OTHER === "de" ? ["ueber_uns"] : [],
  legal: OTHER === "pl"
    ? ["polityka", "kontakt"]
    : OTHER === "de"
      ? ["impressum", "datenschutz", "kontakt_de"]
      : [],
};
// Truong menu cua ngon ngu kia trong file menus (src/_data/menus.json):
// 4 truong de_header/de_footer/pl_header/pl_footer o thu thut 10 khoang.
const DROP_MENU_FIELD = OTHER === "pl"
  ? ["pl_header", "pl_footer"]
  : OTHER === "de"
    ? ["de_header", "de_footer"]
    : [];

const src = path.join(__dirname, "..", "src", "admin", "config.yml");
const dst = path.join(__dirname, "..", "_site", "admin", "config.yml");
const lines = fs.readFileSync(src, "utf8").split("\n");
const kept = [];
for (const ln of lines) {
  if (ln.trimStart().startsWith("#")) continue;
  kept.push(ln);
}
// Gon lai: bo dong trang thua o dau/cuoi, gop nhieu dong trang lien tiep thanh 1
// (dong trang khong anh huong cau truc YAML).
while (kept.length && kept[0].trim() === "") kept.shift();
while (kept.length && kept[kept.length - 1].trim() === "") kept.pop();
const compact = [];
for (const ln of kept) {
  if (ln.trim() === "" && compact.length && compact[compact.length - 1].trim() === "") continue;
  compact.push(ln);
}

// Loc theo ngon ngu (chi khi SITE_LANG duoc dat): bo khoi collection va muc file
// cua ngon ngu kia. Nhan dien khoi bang thu thut:
//   - collection: dong "  - name: <ten>" (2 khoang trang)
//   - muc file trong collection files: dong "      - name: <ten>" (6 khoang trang)
let out = compact;
const droppedCollections = [];
const droppedFiles = [];
const droppedMenuFields = [];
if (OTHER) {
  out = [];
  let currentCollection = "";
  let skipCollection = false; // dang bo ca khoi collection hien tai
  let skipFile = false;       // dang bo ca muc file hien tai
  let skipMenuField = false;  // dang bo ca khoi truong menu cua ngon ngu kia
  for (const ln of compact) {
    // Ket thuc khoi truong menu da bo: dong dau tien co thu thut <= 10
    // (truong anh em, collection moi, ...) — dong trang trong khoi bo qua.
    if (skipMenuField) {
      const indent = (ln.match(/^ */) || [""])[0].length;
      if (ln.trim() === "" || indent > 10) continue;
      skipMenuField = false;
      // roi xuong xu ly dong nay nhu binh thuong
    }
    const colMatch = ln.match(/^  - name: (\S+)\s*$/);
    if (colMatch) {
      currentCollection = colMatch[1];
      skipCollection = DROP_COLLECTION.includes(currentCollection);
      skipFile = false;
      if (skipCollection) {
        droppedCollections.push(currentCollection);
        continue;
      }
      out.push(ln);
      continue;
    }
    // BO CA KHOI collection da bo: cac dong "- name:" 6 khoang ben trong
    // (truong category/draft cua collection truyen) phai bo theo, khong
    // duoc roi xuong nhanh fileMatch ben duoi. (Loi cu: ban pl bo posts_de
    // la collection dau tien nen 2 dong nay roi ra duoi "collections:"
    // lam YAML vo; ban de chi thua 2 truong trung trong posts_de.)
    if (skipCollection) continue;
    const fileMatch = ln.match(/^      - name: (\S+)\s*$/);
    if (fileMatch) {
      const fname = fileMatch[1];
      const dropList = DROP_FILE[currentCollection] || [];
      skipFile = dropList.includes(fname);
      if (skipFile) {
        droppedFiles.push(`${currentCollection}/${fname}`);
        continue;
      }
      out.push(ln);
      continue;
    }
    if (skipFile) continue;
    // Truong menu (10 khoang trang) trong file menus: bo ca khoi cua
    // ngon ngu kia (de_header/de_footer hoac pl_header/pl_footer).
    const menuMatch = ln.match(/^          - name: (\S+)\s*$/);
    if (menuMatch) {
      if (DROP_MENU_FIELD.includes(menuMatch[1])) {
        droppedMenuFields.push(menuMatch[1]);
        skipMenuField = true;
        continue;
      }
      out.push(ln);
      continue;
    }
    out.push(ln);
  }
}

fs.mkdirSync(path.dirname(dst), { recursive: true });
fs.writeFileSync(dst, out.join("\n") + "\n");
console.log(`strip-admin-config: ${src} -> ${dst} (bo ${lines.length - out.length} dong: binh luan + dong trang thua${OTHER ? ` + loc admin ${SITE_LANG} (bo collection: ${droppedCollections.join(", ") || "khong co"}; bo muc file: ${droppedFiles.join(", ") || "khong co"}; bo truong menu: ${droppedMenuFields.join(", ") || "khong co"})` : ""})`);
