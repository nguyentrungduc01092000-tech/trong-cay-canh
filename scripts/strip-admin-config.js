// strip-admin-config.js — Bo dong binh luan (#) khoi src/admin/config.yml
// khi build, de file config.yml trien khai chi chua cau hinh (Ruler 11:50
// 27/11: config.yml live lo ghi chu noi bo tieng Viet). Chay sau eleventy
// (passthrough da copy ban co chu thich vao _site/admin/), ghi de bang ban
// sach. Ban goc co chu thich o src/admin/config.yml GIU NGUYEN (nguon duy
// nhat, khong sua tay ban sach). Cong kiem muc 12 kiem lai tren _site.
const fs = require("fs");
const path = require("path");
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
const out = [];
for (const ln of kept) {
  if (ln.trim() === "" && out.length && out[out.length - 1].trim() === "") continue;
  out.push(ln);
}
fs.mkdirSync(path.dirname(dst), { recursive: true });
fs.writeFileSync(dst, out.join("\n") + "\n");
console.log(`strip-admin-config: ${src} -> ${dst} (bo ${lines.length - out.length} dong: binh luan + dong trang thua)`);
