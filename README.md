# Web truyện hư cấu đa ngôn ngữ — DE + PL (Demo)

Demo web tĩnh cho 2 web truyện hư cấu (tiếng Đức + tiếng Ba Lan), chạy trên
GitHub Pages. Một codebase, hai ngôn ngữ, cùng bộ chủ đề (30 chủ đề trong
`../ban-giao/30-CHU-DE.md`) và cùng hồ sơ phong cách
(`../ban-giao/HO-SO-PHONG-CACH.md`).

> **Trạng thái:** bản demo chạy được cục bộ, **CHƯA đẩy lên repo nào, CHƯA bật
> Pages, CHƯA gắn tên miền**. Mọi chỗ cần Ruler điền thông tin thật đều ghi
> `[GIỮ CHỖ — ...]`. Không có token/secret/mật khẩu nào trong repo.

## 1. Vì sao chọn Eleventy + Sveltia CMS

| Lựa chọn | Lý do |
|---|---|
| **Eleventy 3.1.8** (thay vì Hugo) | Hugo **không có trên máy này**; Eleventy có sẵn trên npm (3.1.8, kiểm chứng `npm view`), chạy trên Node 24 có sẵn, output HTML tĩnh thuần, build nhanh (~5 giây), hỗ trợ tốt đa ngôn ngữ qua collections + data file theo thư mục, filter ngày bản địa bằng `Intl` có sẵn. Không cần học Go template. |
| **Sveltia CMS 0.272.0** (ưu tiên, không phải Decap) | Sveltia là bản kế tiếp của Decap/Netlify CMS, cùng định dạng `config.yml` (tương thích Decap nên chuyển đổi dễ), giao diện hiện đại hơn, vẫn dùng backend GitHub + đăng nhập bằng token cá nhân. Đã kiểm chứng CDN jsDelivr trả 200 cho đúng phiên bản 0.272.0 ngày 25/11/2026. **Chưa đổi sang Decap vì Sveltia qua CDN không gặp lỗi.** |
| **@11ty/eleventy-img 7.1.1** | Nén ảnh ở bước build: mỗi ảnh sinh 3 cỡ (400/800/1200w) × 3 định dạng (AVIF/WebP/JPEG), ảnh gốc vẫn giữ trong `src/media/` và copy ra `/media/`. |
| **GoatCounter** (thống kê) | Miễn phí, không cookie, đúng chuẩn EU; chỉ tải sau khi người đọc đồng ý (xem mục 5). |

## 2. Cấu trúc

```text
site/
├── eleventy.config.js      # collections DE/PL, filter ngày bản địa, shortcode ảnh
├── package.json            # npm run build / serve
├── src/
│   ├── _data/
│   │   ├── settings.json   # tên site, logo, màu, GoatCounter, câu hư cấu (sửa qua CMS)
│   │   └── categories.json # 6 chuyên mục DE/PL (sửa qua CMS)
│   ├── _includes/layouts/  # base.njk, post.njk, page.njk
│   ├── assets/css/style.css, assets/js/search.js, assets/js/cookie.js
│   ├── de/                 # de.json (chuỗi giao diện + locale de-DE)
│   │   ├── index.njk       # trang chủ DE: lưới thẻ bài + ô tìm kiếm + nav chuyên mục
│   │   ├── kategorie.njk   # phân trang theo categories.json → /de/kategorie/<key>/
│   │   ├── kontakt.md      # Liên hệ DE (khung giữ chỗ, Ruler điền thật)
│   │   ├── posts/*.md      # truyện DE (frontmatter đầy đủ, xem mục 3)
│   │   ├── impressum.md, datenschutz.md, ueber-uns.md
│   │   └── search.json.njk # chỉ mục tìm kiếm JSON sinh ở bước build
│   ├── pl/                 # pl.json (locale pl-PL), posts, polityka-prywatnosci,
│   │                       # kontakt, o-nas, kategoria.njk → /pl/kategoria/<key>/,
│   │                       # search.json.njk — cấu trúc như DE
│   ├── media/covers/       # ảnh gốc tải lên qua CMS (đi vào /media/)
│   ├── admin/index.html    # Sveltia CMS (CDN) + config.yml
│   ├── dashboard.njk       # trang /dashboard/ — thống kê build-time
│   └── index.njk           # / → chuyển sang /de/
└── .github/workflows/
    ├── deploy-pages.yml    # build + deploy Pages khi push main
    └── scheduled-build.yml # cron 06:00 + 18:00 UTC rebuild (bài hẹn giờ tự lên)
```

**Frontmatter mỗi truyện:** `title, slug, description, cover, images, category,
tags, date, author, seo_title, seo_description, draft` (+ `layout`,
`permalink: /de/{{ slug }}/` hoặc `/pl/{{ slug }}/`).

**Quy tắc xuất bản (trong `eleventy.config.js`):**
- `draft: true` → không xuất bản.
- `date` trong tương lai → không xuất bản cho tới khi rebuild sau ngày đó
  (workflow `scheduled-build.yml` rebuild 2 lần/ngày để bài hẹn giờ tự lên).
- Ngày hiển thị dạng bản địa qua `Intl.DateTimeFormat` (`de-DE`:
  "25. November 2026"; `pl-PL`: "25 listopada 2026").

**Trang chủ mỗi ngôn ngữ:** lưới thẻ bài (ảnh bìa responsive + tiêu đề + mô tả
ngắn + ngày bản địa + chuyên mục) + ô tìm kiếm client-side đọc chỉ mục JSON
(`/de/search.json`, `/pl/search.json`) sinh ở bước build. Chuyển ngôn ngữ
DE/PL ở đầu trang. Responsive, chỉ 2 file JS nhỏ (tìm kiếm + cookie).

**Danh sách bài trong CMS:** Sveltia CMS hiển thị danh sách entry dạng list có
tìm kiếm/lọc theo trường (theo tài liệu của Sveltia CMS). **Chưa kiểm chứng
bằng tài khoản thật** — Ruler kiểm lại sau khi đăng nhập lần đầu (xem mục 6).
Nếu Sveltia thiếu dạng bảng như yêu cầu, ghi rõ ở đây sau khi kiểm chứng;
config dùng chung định dạng Decap nên có thể đổi sang Decap mà không sửa
cấu trúc nội dung.

## 3. Chạy cục bộ

```bash
cd site
npm install
npm run build    # build ra _site/
npm run serve    # http://localhost:8080
```

## 4. CMS admin (`/admin/`)

- Mở `/admin/` → đăng nhập bằng **token GitHub do Ruler tự tạo** (xem mục 6).
- Collections: `posts_de`, `posts_pl` (đủ trường: tiêu đề, slug, nội dung,
  mô tả, ảnh bìa + ảnh trong bài, danh mục, thẻ, ngày đăng/hẹn giờ, SEO
  title/description, trạng thái đã đăng/nháp — trạng thái nháp là trường
  `draft`, hẹn giờ là trường `date` trong tương lai), `categories`,
  `legal` (Impressum, Datenschutz, Polityka prywatności, Kontakt),
  `settings` (tên site, logo, màu, menu qua tên site, chân trang — file
  collection sửa `src/_data/settings.json`).
- Ảnh tải lên qua CMS vào `src/media/`; build tự nén ra nhiều cỡ/định dạng.
- **Không ghi token vào `config.yml` hay bất cứ file nào.** Trước khi dùng
  thật, sửa `repo:` trong `src/admin/config.yml` thành repo thật của Ruler
  (hiện là `[GIỮ CHỖ — ...]`).

## 5. Cookie banner + GoatCounter

- Banner hiện ở cuối mọi trang; lựa chọn lưu vào `localStorage`
  (`cookie-consent` = `accepted`/`declined`).
- GoatCounter **chỉ tải sau khi người đọc bấm đồng ý** (script chèn động trong
  `src/assets/js/cookie.js`). Từ chối = không tải gì.
- **Ruler tự tạo tài khoản GoatCounter miễn phí:**
  1. Vào https://www.goatcounter.com → đăng ký tài khoản miễn phí
     (gói miễn phí cho site cá nhân/nhỏ, không cần thẻ).
  2. Khi tạo site, GoatCounter cấp một domain dạng
     `ten-site.goatcounter.com` — ghi lại domain này.
  3. Sửa `src/_data/settings.json`: điền 2 domain — `goatcounter_domain_de`
     = `sunbow.goatcounter.com` (web Đức), `goatcounter_domain_pl`
     = `plasma.goatcounter.com` (web Ba Lan). Mỗi web một mã đúng cặp,
     không nhầm chéo. Chỉ cần domain — không còn cờ `goatcounter_enabled`
     (đã dọn ngày 26/11/2026, COOKIE-ANALYTICS §3 việc 3: cookie.js
     không đọc cờ này, domain giữ chỗ đã đủ chặn tải).
  4. Build lại + deploy. Link 2 trang thống kê GoatCounter hiện ở
     `/dashboard/` sau khi bật.
- Domain đã điền (26/11/2026): DE = sunbow.goatcounter.com, PL =
  plasma.goatcounter.com. `cookie.js` chỉ tải script sau khi người đọc
  đồng ý qua banner; trước đó không tải gì.

## 6. Ruler tự làm — từng bước (chưa làm, cần Ruler)

1. **Tạo repo GitHub + đẩy code:**
   - Tạo repo private/public mới trên GitHub (tên do Ruler chọn), đẩy toàn bộ
     thư mục `site/` lên nhánh `main`. (Agent này KHÔNG đẩy.)
2. **Tạo token GitHub cho CMS (đăng nhập /admin/):**
   - GitHub → Settings → Developer settings → Personal access tokens →
     Tokens (classic) → Generate new token → đặt tên (vd `sveltia-cms`) →
     tick quyền **`repo`** (đọc + ghi repo; nếu repo public chỉ cần
     `public_repo`, nhưng repo này nên để `repo` cho chắc) → tạo, **sao chép
     token ngay** (chỉ hiện 1 lần).
   - Mở `https://<domain>/admin/`, đăng nhập bằng token đó. Token chỉ nằm
     ở trình duyệt của Ruler, không lưu trong repo.
   - Trước đó sửa `repo:` trong `src/admin/config.yml` thành
     `tên-tài-khoản/tên-repo` thật rồi push.
3. **Bật GitHub Pages:**
   - Repo → Settings → Pages → Build and deployment → Source:
     **GitHub Actions** (không chọn "Deploy from a branch").
   - Push code lên `main` → workflow `deploy-pages.yml` chạy → site lên tại
     `https://<tài-khoản>.github.io/<repo>/`.
   - Workflow `scheduled-build.yml` tự chạy 06:00 + 18:00 UTC (cron miễn phí
     của GitHub Actions cho repo public; repo private vẫn có 2.000 phút
     miễn phí/tháng — build này ~1 phút/lần nên đủ).
4. **Tạo tài khoản GoatCounter:** xem mục 5 (3 bước).
5. **Đổi DNS (tên miền riêng sunbow.click / plasma.click):**
   - Domain thật đã điền vào demo (26/11/2026, Ruler chốt): DE =
     sunbow.click, PL = plasma.click — trong `settings.json`
     (`site_url_de` / `site_url_pl`), sitemap/robots/canonical theo
     đúng cặp. Vẫn **chưa chạm repo/tên miền thật** (không đẩy, không
     đổi DNS) cho tới khi Ruler duyệt demo.
   - Khi triển khai: vào repo → Settings → Pages → Custom domain →
     nhập tên miền → chờ GitHub cấp chứng chỉ HTTPS; ở nhà đăng ký
     tên miền (Tenten) tạo bản ghi CNAME trỏ về `<tài-khoản>.github.io`
     (hoặc 4 bản ghi A của GitHub Pages nếu dùng apex domain). Kiểm
     lại sau 1–2 giờ.
   - Mô hình đã chốt (26/11/2026): 2 web DE/PL **dùng chung 1 codebase
     nhưng là 2 site riêng** (2 repo hoặc 2 lần deploy), mỗi web một
     tên miền.
6. **Điền thông tin thật vào trang pháp lý:** Impressum, Datenschutz,
   Polityka prywatności, Kontakt (các chỗ `[GIỮ CHỖ — ...]`).
7. **Kiểm lại danh sách bài trong CMS** sau khi đăng nhập lần đầu (xem mục 2).

## 7. Gắn 6 truyện thật + ảnh (khi có đủ nội dung)

**Điều phối viên chép file như sau (không cần sửa code):**

```bash
# 1. Truyện DE (3 truyện mẫu: chủ đề 3, 8, 17) — file .md theo đúng frontmatter mục 2
cp /home/hatch/workspace/truyen-de-pl/noi-dung/<ten-file-de>.md  site/src/de/posts/
# 2. Truyện PL (3 truyện mẫu)
cp /home/hatch/workspace/truyen-de-pl/noi-dung/<ten-file-pl>.md  site/src/pl/posts/
# 3. Ảnh bìa + ảnh trong bài (đã tạo sẵn theo prompt)
cp /home/hatch/workspace/truyen-de-pl/site/assets/images/*  site/src/media/
#    rồi sửa trường cover/images trong frontmatter trỏ tới src/media/<ten-anh>
# 4. Build + kiểm tra
npm run build && npm run serve
```

Yêu cầu file truyện thật: 900–1.200 từ, ngôi thứ nhất, tiêu đề móc 12–20 từ,
`slug` chữ thường không dấu, `date` đúng ngày đăng (hoặc tương lai để hẹn giờ),
`category` đúng 1 trong 6 chuyên mục **theo đúng tên trong
`src/_data/categories.json`** (DE: Familie/Nachbarschaft/Arbeitswelt/
Freundschaft/Haustiere/Gemeinschaft; PL: Rodzina/Sąsiedzi/Praca/Przyjaźń/
Zwierzęta/Wspólnota — lưu ý: tên PL là "Zwierzęta", không phải "Zwierzęta
domowe" như bảng 30-CHU-DE.md; tên DE là "Nachbarschaft"/"Arbeitswelt",
không phải "Nachbarn"/"Arbeit". Sai tên = truyện không vào được trang
chuyên mục), `cover` trỏ tới file trong `src/media/`.
Xóa 2 file truyện mẫu (`hund-am-gartentor.md`, `notatnik-na-lawce.md`) khi
truyện thật đã vào.

## 8. Chưa làm ở bản đầu (theo yêu cầu)

- Comments (bình luận), AI Translation (dịch máy), Site Health (kiểm tra sức
  khỏe site tự động).
- Kiểm chứng CMS bằng tài khoản thật (cần token + repo thật của Ruler).
- Tên miền riêng, Search Console, AdSense — ngoài phạm vi bản demo này.

## 9. Hoàn thiện khung site + giao diện (26/11/2026, theo lệnh Ruler 09:55)

- **Trang chuyên mục:** 12 trang (`/de/kategorie/<key>/`,
  `/pl/kategoria/<key>/`, phân trang từ `categories.json`, mỗi trang có tiêu
  đề bản địa + số bài + câu báo trống khi chưa có truyện). Nav chuyên mục
  (tên + số bài) ở đầu trang chủ mỗi ngôn ngữ; tên chuyên mục trên thẻ bài
  và trang truyện link tới trang chuyên mục. Filter mới trong
  `eleventy.config.js`: `categoryUrl`, `postsInCategory`, `categoryCount`.
- **Trang Liên hệ DE:** `src/de/kontakt.md` mới (khung giữ chỗ như bản PL) +
  link Kontakt trong footer DE + mục `kontakt_de` trong `src/admin/config.yml`.
- **Tìm kiếm:** đã sửa lỗi `normalize()` trong `search.js` — NFD không tách
  được "ł" (và "ß") nên gõ không dấu ("lawce") không tìm ra "ławce"; nay thay
  tay `ł→l`, `ß→ss`. Kiểm chứng bằng trình duyệt thật: PL "lawce"/"ławce"/
  "notatnik"/"pies" đều ra đúng 1/3 thẻ; DE "Hund" ra đúng 1/4 thẻ; gõ sai
  hiện câu "không tìm thấy".
- **Build:** `npm run build` 0 lỗi, Wrote 33 files, **31 trang HTML**
  (18 cũ + 12 chuyên mục + 1 kontakt DE). Build tăng dần bình thường ~1–2
  giây (không `rm -rf _site`); một lần _site bị mất toàn bộ HTML đã sinh
  (giữa 2 lần build, nguyên nhân chưa rõ — nghi một tiến trình khác chạm
  vào thư mục) nên lần build sau phải xử lý lại toàn bộ ảnh: 170 giây.
  Bài học: sau mỗi lần build, kiểm tra lại `_site` còn đủ trang trước khi
  kết luận; ảnh đã sinh trong `_site/img/` đầy đủ (114 file, 13 ảnh gốc ×
  9 biến thể, riêng ảnh bìa 526px chỉ có 6 biến thể vì không phóng to).
- **Kiểm chứng 26/11/2026** (xem KIEM-CHUNG.md mục 5): curl 200 cho 17/17
  URL (trừ 1 URL thử sai `/pl/kategoria/praca/` — key đúng là
  `arbeitswelt`); ngày bản địa DE "25./26. November 2026", PL
  "25 listopada 2026"; di động 390px: 5 trang scrollWidth = 390, 0 tràn,
  0 lỗi console; cookie banner có mặt.
- **Còn để điều phối viên/Ruler quyết (không tự xử):** truyện
  "Schwiegermutter/Hausordnung" (12.496 từ, nhiều tập "Tập 1…", thể loại
  xung đột gia đình) đã có trong site từ trước — vượt chuẩn 900–1.200 từ
  và thuộc nhóm §10 hồ sơ phong cách ghi KHÔNG học theo; W-13 chỉ giữ
  nguyên, không xóa, không sửa nội dung.

## 10. Sửa 3 mục cổng Q-17 lần 1 (26/11/2026, lệnh điều phối viên, trước 14:00)

- **(13) 1 H1/trang + meta description:** xóa dòng `# ...` đầu thân bài trong
  7 file `.md` (4 truyện DE + ueber-uns + o-nas + pl-03 zagubiony-pies);
  pl-08/pl-17 vốn không có dòng H1 trong `.md` nên không chạm vào. Thêm
  `description` cho `/dashboard/` (trước đây meta rỗng vì trang này không
  thừa hưởng tagline của de/pl). Tổng số từ (thân + tiêu đề) sau khi xóa
  dòng `#` vẫn trong 900–1.200 (de-03 1.077, de-08 1.163, de-17 937,
  pl-03 1.019, pl-08 995, pl-17 912) vì tiêu đề chỉ còn đếm 1 lần.
- **(15) Sitemap + robots:** `src/sitemap.xml.njk` (permalink `/sitemap.xml`)
  + `src/robots.txt.njk` (permalink `/robots.txt`), sinh ở bước build.
  Sitemap liệt kê 29 URL (mọi trang HTML trừ `/admin/` — trang quản trị
  CMS không đưa vào sitemap — và trang chuyển hướng `/`); robots cho phép
  hết, `Disallow: /admin/`. Domain trong sitemap lấy từ `site_url_de`
  (sunbow.click, trang /de/ + /dashboard/) và `site_url_pl`
  (plasma.click, trang /pl/) trong `settings.json`, sửa được qua CMS
  mục Settings; robots liệt kê cả 2 sitemap. Lưu ý kỹ thuật:
  `collections.all` của Eleventy chỉ
  chứa trang ĐẦU của mỗi template phân trang, nên 12 trang chuyên mục được
  liệt kê riêng từ `categories.json` (không dùng `collections.all` cho
  chúng); và Nunjucks dùng `endsWith` (chữ W hoa), không phải `endswith`.
- **(21) 3 việc cookie (COOKIE-ANALYTICS §3):** (1) link rút lại đồng ý
  (`Cookie-Einstellungen` / `Ustawienia plików cookie`, `id="cookie-settings"`)
  trong footer-nav của `base.njk` + đoạn JS trong `cookie.js` (bấm → xóa
  `localStorage` → banner hiện lại); (2) link tới trang bảo mật trong
  banner (đoạn `cookie-more`, link tới Datenschutz / Polityka prywatności);
  (3) dọn cờ `goatcounter_enabled` khỏi `settings.json` + `config.yml`
  (cách A), đồng thời sửa `dashboard.njk` (bỏ điều kiện cờ + bỏ câu hướng
  dẫn bật cờ) và README mục 5 — cookie.js vốn không đọc cờ này. Thêm
  `site_url` vào `settings.json` + CMS Settings (cho sitemap/robots).
- **(17)/(18) KHÔNG sửa theo lệnh:** trang pháp lý DE/PL vẫn là bản ngắn
  ban đầu (kể cả 2 trích dẫn luật cũ § 5 TMG / § 55 RStV trong Impressum)
  — bản hoàn thiện PHAP-LY-DE.md / PHAP-LY-PL.md chờ Ruler điền giữ chỗ +
  duyệt rồi mới chép vào site.
- **Kiểm chứng:** cổng Q-17 chạy lại cùng ngày: **21 ĐẠT / 2 TRƯỢT
  (chỉ 17/18) / 1 CHƯA XÁC MINH (mục 16 mobile — script không chạy
  Playwright)**; quét chữ cấm 0 lượt thật. Kiểm tay bằng trình duyệt thật:
  banner hiện lần đầu → Từ chối (localStorage=declined, 0 request thống
  kê) → bấm link footer → banner hiện lại (localStorage xóa) → Đồng ý
  (localStorage=accepted, 0 request vì domain còn giữ chỗ) → tải lại vẫn
  ẩn; 0 lỗi console. Mobile 390px: 5 trang nội dung scrollWidth=390,
  0 tràn; `/dashboard/` tràn 117px (bảng thống kê rộng — ghi chú đã biết
  của Q-17, trang nội bộ, chưa sửa). JSON cổng sau sửa:
  `~/workspace/sua-cong-q17-2026-11-26/KIEM-CONG-SAU-SUA-2026-11-26.json`
  (không ghi đè JSON gốc của Q-17). Snapshot file trước khi sửa:
  `~/workspace/sua-cong-q17-2026-11-26/`.
