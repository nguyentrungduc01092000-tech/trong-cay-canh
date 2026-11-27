# KIỂM CHỨNG — Demo web truyện DE/PL (Eleventy + Sveltia CMS)

Ngày kiểm chứng: 25/11/2026 (giờ +07). Máy: Node v24.22.1, npm 10.9.4,
Python 3.12.3. Phiên bản: @11ty/eleventy 3.1.8, @11ty/eleventy-img 7.1.1,
@sveltia/cms 0.272.0 (CDN jsDelivr, kiểm chứng trả 200).

## 1. Build

- Lệnh: `npm run build` trong `/home/hatch/workspace/truyen-de-pl/site/`
- Kết quả: **PASS — 0 lỗi, Wrote 15 files** (lần build cuối sau khi rút ngắn
  truyện mẫu; lần đầu lỗi `Image is not a function` vì eleventy-img v7 là
  ESM — đã sửa bằng `.default` khi require, build lại PASS).
- Ảnh sinh bởi eleventy-img: mỗi ảnh bìa 3 cỡ (400/800/1200w) × 3 định dạng
  (AVIF/WebP/JPEG) = 18 file trong `_site/img/`; ảnh gốc giữ nguyên trong
  `_site/media/covers/` (hund.jpg 36 KB → hund-1200w.avif 8 KB).

## 2. Server cục bộ + curl (python3 -m http.server trên _site/)

| # | Kiểm tra | Kết quả |
|---|---|---|
| 1 | Trang chủ DE `/de/` trả 200 + chứa tiêu đề truyện DE | PASS (200; "Der Hund, der jeden Abend an unserem Gartentor wartete" có mặt) |
| 2 | Trang chủ PL `/pl/` trả 200 + chứa tiêu đề truyện PL | PASS (200; "Notatnik, który ktoś zostawił na ławce w parku" có mặt) |
| 3 | Truyện DE `/de/hund-am-gartentor/` trả 200 + chứa đúng `<h1>` | PASS (200; `<h1>` khớp) |
| 4 | Truyện PL `/pl/notatnik-na-lawce/` trả 200 + chứa đúng `<h1>` | PASS (200; `<h1>` khớp) |
| 5 | `/admin/` trả 200 + chứa thẻ script CMS | PASS (200; chứa `sveltia-cms.js` — CDN @sveltia/cms 0.272.0) |
| 6 | `/dashboard/` trả 200 | PASS (200; chứa bảng thống kê build-time) |
| 7 | `/de/search.json` + `/pl/search.json` trả 200, JSON hợp lệ | PASS (mỗi file 1 entry, đúng tiêu đề) |
| 8 | Ngày bản địa trên trang chủ | PASS (DE: "25. November 2026"; PL: "25 listopada 2026") |
| 9 | Câu tuyên bố hư cấu ở chân trang | PASS (DE + PL đều có mặt) |
| 10 | Cookie banner + GoatCounter giữ chỗ | PASS (banner có mặt; `data-goatcounter` là chuỗi giữ chỗ nên không tải script thống kê) |

## 3. Nội dung mẫu

- DE: `src/de/posts/hund-am-gartentor.md` — "Der Hund, der jeden Abend an
  unserem Gartentor wartete", ~199 từ thân bài (đo bằng Python split, không
  tính frontmatter + dòng ghi chú mẫu). Chủ đề 3 (chú chó đi lạc).
- PL: `src/pl/posts/notatnik-na-lawce.md` — "Notatnik, który ktoś zostawił
  na ławce w parku", ~197 từ thân bài. Chủ đề 8 (cuốn sổ tay trên ghế đá).
- Cả hai ghi rõ "NỘI DUNG MẪU — sẽ thay bằng 6 truyện thật", ngôi thứ nhất,
  kết trọn vẹn, không sao chép web mẫu. (Mục tiêu ~150 từ; thực tế ~200 từ
  vì câu tiếng Đức/Ba Lan dài — vẫn ngắn hơn nhiều so với chuẩn 900–1.200 từ.)

## 4. Chưa kiểm chứng được ở bản demo (cần Ruler)

- Đăng nhập CMS thật bằng token GitHub (cần repo + token thật).
- Deploy GitHub Pages thật, workflow cron thật, tên miền riêng.
- GoatCounter thật (cần tài khoản + domain thật).

## 5. Hoàn thiện khung site + giao diện — kiểm chứng 26/11/2026 (lệnh Ruler 09:55)

- **Build:** `npm run build` trong `site/` — **PASS, 0 lỗi, Wrote 33 files**
  (build tăng dần cuối: 1,15 giây; không `rm -rf _site`). **31 trang HTML**
  trong `_site/` (18 cũ + 12 trang chuyên mục + 1 trang Liên hệ DE).
  Ảnh: `_site/img/` đủ 114 file (13 ảnh gốc × 9 biến thể; riêng ảnh bìa
  Schwiegermutter rộng 526px chỉ có 6 biến thể vì eleventy-img không phóng to).
- **Trang chuyên mục (12 trang):** tiêu đề đúng (`Kategorie: Familie | …`,
  `Kategoria: Zwierzęta | …`); số thẻ đúng từng trang — DE Familie 2,
  Gemeinschaft 1, Haustiere 1, 3 trang còn lại 0 + câu báo trống; PL Rodzina
  1, Wspólnota 1, Zwierzęta 1, 3 trang còn lại 0 + câu báo trống. Tổng 4 + 3
  = đủ 7 truyện đã đăng. Nav chuyên mục ở trang chủ DE/PL đủ 6 link kèm số
  bài; tên chuyên mục trên thẻ bài và trang truyện đều link đúng trang.
- **Trang Liên hệ DE:** `/de/kontakt/` trả 200; link Kontakt có trong footer
  DE; mục `kontakt_de` đã thêm vào `src/admin/config.yml`.
- **Tìm kiếm (trình duyệt thật, Chromium):** DE "Hund" → 1/4 thẻ; gõ sai →
  hiện câu "Keine Geschichten gefunden."; PL "lawce" (không dấu) → 1/3 thẻ,
  "ławce" → 1/3, "notatnik" → 1/3, "pies" → 1/3. **Lỗi đã sửa:** `normalize()`
  trong `search.js` chỉ dùng NFD nên "ł" không tách được (không có dạng phân
  tách chuẩn) — gõ "lawce" ra 0 kết quả; đã thay tay `ł→l`, `ß→ss`, kiểm lại
  PASS cả 4 truy vấn PL + DE.
- **Ngày bản địa:** trang chủ DE "25. November 2026" ×3 + "26. November 2026"
  ×1; PL "25 listopada 2026" ×3.
- **Di động 390px (Playwright):** `/de/`, `/pl/`, `/de/kategorie/familie/`,
  truyện DE, `/de/kontakt/` — `scrollWidth` = 390 cả 5 trang, 0 tràn.
  Console errors: 0 (desktop + mobile). Cookie banner có mặt.
- **HTTP cục bộ (python http.server trên `_site/`):** 17/17 URL trả 200
  (trang chủ, truyện, chuyên mục, Giới thiệu, Liên hệ, search.json,
  dashboard, admin). 1 URL thử sai `/pl/kategoria/praca/` trả 404 — đúng
  vì key chuyên mục là `arbeitswelt` (tên hiển thị PL mới là "Praca").
- **Sự cố _site:** giữa 2 lần build, toàn bộ HTML đã sinh trong `_site/`
  biến mất (chỉ còn passthrough admin/assets/media + ảnh img/), nguyên nhân
  chưa xác định — build lại đầy đủ (170 giây do xử lý lại toàn bộ ảnh) và
  kiểm lại đủ 31 trang sau 20 giây vẫn còn nguyên. Không mất file nguồn
  nào (`src/` nguyên vẹn). Đã ghi vào README mục 9.
- **Sửa 1 dòng frontmatter:** `src/pl/posts/zagubiony-pies-wraca-do-domu.md`
  `category: Zwierzęta domowe` → `Zwierzęta` cho khớp `categories.json` +
  CMS config (tên trong 30-CHU-DE.md khác tên site ở 3 chỗ:
  Nachbarn/Arbeit/Zwierzęta domowe ↔ Nachbarschaft/Arbeitswelt/Zwierzęta —
  để điều phối viên quyết có đổi tên hiển thị không; truyện không khớp tên
  sẽ không vào được trang chuyên mục).

## 6. Sửa 3 mục cổng Q-17 lần 1 — kiểm chứng 26/11/2026 (trước 14:00)

- **(13) 1 H1/trang + meta:** xóa dòng `# ...` trong 7 file `.md` (4 truyện
  DE + ueber-uns + o-nas + pl-03); pl-08/pl-17 không chạm; thêm
  `description` cho `/dashboard/`. Cổng kiểm lại: trang H1≠1 = 0, thiếu
  meta description = 0; độ dài tổng sau sửa vẫn 900–1.200 (de-03 1.077,
  de-08 1.163, de-17 937, pl-03 1.019, pl-08 995, pl-17 912).
- **(15) Sitemap + robots:** `src/sitemap.xml.njk` + `src/robots.txt.njk`
  sinh ở bước build; sitemap 29 URL (trừ `/admin/` + trang chuyển hướng
  `/`); robots `Allow: /` + `Disallow: /admin/` + dòng Sitemap. Domain lấy
  từ `site_url` trong `settings.json` (còn giữ chỗ, Ruler điền sau).
  Lưu ý: `collections.all` chỉ chứa trang đầu của template phân trang nên
  12 trang chuyên mục liệt kê riêng từ `categories.json`.
- **(21) Cookie:** link rút đồng ý ở footer (`id="cookie-settings"`,
  29/29 trang công khai đều có) + link bảo mật trong banner (cả 2 ngôn
  ngữ) + dọn cờ `goatcounter_enabled` khỏi `settings.json` + `config.yml`
  (+ sửa `dashboard.njk` cho khớp). Kiểm tay trình duyệt thật: Từ chối →
  banner ẩn, localStorage=declined, 0 request thống kê; bấm link footer →
  banner hiện lại, localStorage xóa; Đồng ý → localStorage=accepted,
  0 request (domain còn giữ chỗ); tải lại vẫn ẩn; 0 lỗi console.
- **Cổng chạy lại:** **21 ĐẠT / 2 TRƯỢT (17/18 — pháp lý, KHÔNG sửa theo
  lệnh, chờ Ruler) / 1 CHƯA XÁC MINH (mục 16 mobile — script không chạy
  Playwright)**; quét chữ cấm 0 lượt thật. JSON sau sửa:
  `~/workspace/sua-cong-q17-2026-11-26/KIEM-CONG-SAU-SUA-2026-11-26.json`.
- **Mobile 390px (Playwright, kiểm tay):** 5 trang nội dung scrollWidth =
  390, 0 tràn, 0 lỗi console; `/dashboard/` scrollWidth = 507 (tràn 117px
  — ghi chú đã biết của Q-17, trang nội bộ, chưa sửa).
- **(17)/(18) không sửa:** trang pháp lý vẫn bản ngắn + 2 trích dẫn luật
  cũ (§ 5 TMG / § 55 RStV) — chờ Ruler điền giữ chỗ + duyệt bản hoàn
  thiện rồi mới chép vào site.
