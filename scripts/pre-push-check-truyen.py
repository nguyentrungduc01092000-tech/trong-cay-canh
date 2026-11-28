#!/usr/bin/env python3
"""Kiem tra TRUOC KHI DAY cho 2 web truyen DE/PL (sunbow.click / plasma.click).
Nhom D, 26/11/2026 — CHUA day, chi chuan bi.

Usage:
  pre-push-check-truyen.py [--site-dir PATH] [--expect N] [--expect-de N] [--expect-pl N] [--no-build] [--domain DOMAIN]
    --site-dir : thu muc site/ (mac dinh: ../site ke tu file script)
    --expect / --expect-de / --expect-pl : so truyen truyen ro CHI DE DOI CHIEU
        (khong bat buoc); cong TU DEM so truyen tu file .md nguon trong repo
        (src/<lang>/posts/*.md) lam chuan — them/xoa truyen khong can sua cong.
    --no-build : bo qua buoc build (dung khi _site vua build xong va src/ chua doi)
    --domain   : kiem them file CNAME cua repo nay (sunbow.click hoac plasma.click)

Kiem (moi muc DAT moi cho phep day; 1 muc TRUOT = CHAN day):
  0. Build: npm run build exit 0 (build tang dan, KHONG rm -rf _site; khi co
     --domain/SITE_LANG thi truyen SITE_LANG vao build va xoa tay thu muc cu
     cua ngon ngu kia trong _site truoc khi build — build tang dan khong tu
     xoa file cu).
  1. So truyen: so truyen da build phai bang so file .md nguon (tu dem tu
     repo); file .md nguon khop so truyen da build (truyen nhap/hen gio chua
     len se bi neu ten); moi URL truyen co trong sitemap. (Phuong an A) Ngon
     ngu kia KHONG build: phai co 0 truyen
     da build nhung file .md nguon van phai con (chung minh khong xoa khoi repo).
  2. Sitemap (Phuong an A): XML hop le; KHI CO --domain (hoac SITE_LANG):
     chi URL cua domain do — sunbow = truyen DE + 10 (trang chu DE +
     dashboard + 4 phap ly DE + 4 chuyen muc DE), plasma = truyen PL + 8
     (trang chu PL + 3 phap ly PL + 4 chuyen muc PL); URL domain kia = truot.
     KHI KHONG CO --domain: ban gop cu (tong = DE + PL + 18).
  3. robots.txt: Allow /; chi Disallow /admin/; KHI CO --domain: dung 1 dong
     Sitemap cua domain do; KHI KHONG CO --domain: dung 2 dong theo thu tu
     [sunbow, plasma]; khong chan bot quang cao/Googlebot.
  4. Canonical: moi file HTML (tru admin/index.html + 2 trang admin noi bo
     /admin/chia-se/ + /admin/thong-ke/) co dung 1 canonical
     tuyet doi, dung domain theo ngon ngu (/de/* + /dashboard/ -> sunbow,
     /pl/* -> plasma; trang goc / -> https://sunbow.click/de/ o ban de,
     https://plasma.click/pl/ o ban pl); khong co canonical tro
     github.io/localhost/domain khac.
  5. Email that: nguyentrungduc01092000@gmail.com CHI o trang phap ly cua
     ngon ngu do (ban de: de/impressum, de/datenschutz, de/kontakt; ban pl:
     pl/kontakt, pl/polityka-prywatnosci) va du ca trang; ten "Nguyen Trung
     Duc" (khong dau) du o Impressum/Datenschutz (ban de) / Polityka
     (ban pl); "Nguyễn Trung Đức" (co dau) = 0; tu "Ruler" = 0 trong chu
     hien thi (quyet Ruler 14:00/14:02/14:08).
  6. AdSense BAT (Ruler 11:42 27/11): moi HTML dung base.njk dung 1 lan
     "ca-pub-1934454305970765"; admin/index.html + 2 trang admin noi bo
     (/admin/chia-se/, /admin/thong-ke/) + index.html (trang chuyen
     huong, khong dung base.njk) = 0; ads.txt ton tai dung 1 dong; khong co
     file xac minh google*.html.
  7. Giu cho: "[GIỮ CHỖ]" = 0 trong chu hien thi HTML + sitemap/robots;
     repo trong admin/config.yml (ca src/ lan _site/) phai la owner/repo that,
     khong duoc chua "GIỮ CHỖ". NGOAI LE CO TINH: cookie.js co chuoi "GIỮ CHỖ"
     trong comment + lenh bao ve (khong tai GoatCounter khi domain la giu cho)
     — giong co che cua cong kiem (giu_cho_goatcounter_attr), khong tinh vi pham.
  8. Allowlist: _site chi chua loai file duoc phep (.html/.css/.js/.json/.xml/
     .txt/.svg/.webp/.avif/.jpeg/.jpg/.png/.gif/.ico/CNAME); khong co .md,
     khong co node_modules; admin/config.yml phai co.
  9. CNAME/workflow: file CNAME o goc repo (workflow copy vao _site) chi chua
     dung 1 domain; CA 2 workflow (deploy-pages.yml + scheduled-build.yml)
     phai co buoc copy CNAME, buoc kiem chung sitemap/robots theo domain
     (split-sitemap-robots — Ruler 08:50 27/11: moi domain chi co
     sitemap/robots cua chinh no) VA buoc dat SITE_LANG theo CNAME (Phuong
     an A — neu khong, rebuild dinh ky se dua ban gop len live lai).
     (Chua co repo thi muc nay TRUOT — dung, doi Ruler tao repo + dien CNAME.)
 10. Cau hu cau: moi trang truyen + 2 trang chu deu co cau tuyen bo hu cau
     dung ngon ngu (DE "Alle Geschichten auf dieser Website sind frei
     erfunden." / PL "Wszystkie historie na tej stronie są fikcją.").
 11. Anh bia (Ruler 07:41 ngay 27/11 — demo tach anh ra assets lam anh Duc
     chi thay alt): moi bai .md co truong cover tro toi file that trong src/
     (kich thuoc > 0); moi <img> tren trang chu + trang danh muc + trang
     truyen deu tro toi file that trong _site (kich thuoc > 0). Sau khi day,
     chay lai muc nay bang kiem-anh-bia.py --base https://sunbow.click (va
     https://plasma.click) de kiem anh that tren live (trinh duyet do
     naturalWidth > 0, 0 anh vo).
 12. Admin sach (Ruler 11:50 27/11 — config.yml live lo ghi chu noi bo):
     moi file duoi _site/admin/ co 0 dong bat dau bang # (sau khoang trang
     dau dong), 0 chu thich HTML <!-- -->, 0 tu "Ruler"/"GIỮ CHỖ"; trang
     admin co meta noindex; robots.txt Disallow /admin/ (muc 3 kiem robots).
 13. Mot ngon ngu moi web (Phuong an A, Ruler 15:52 27/11 — CHI chay khi co
     --domain hoac SITE_LANG): _site KHONG co thu muc/trang cua ngon ngu kia
     (ke ca /dashboard/ o ban pl); 0 link noi bo (href) toi ngon ngu kia;
     0 chuoi domain kia trong HTML da dung; khong con nut chuyen ngon ngu
     (lang-switch); canonical moi trang tu tro ve domain dang kiem;
     admin da dung chi co collection posts cua ngon ngu do + du About/Legal
     cua ngon ngu do; config nguon van du ca 2 collection (chung minh khong
     xoa khoi repo).
 14. Front matter cua file do CMS tao (Ruler 10:14 28/11): moi bai .md phai
     co date chi ngay (khong gio), slug [a-z0-9-]+, cover tro toi file that
     (chap nhan ca src/media/ va /media/), permalink neu co phai dung
     /<lang>/<slug>/ hoac mau /<lang>/{{ slug }}/ (thieu thi OK — build tinh
     tu slug), layout dung, tags neu co phai la list (thieu thi OK — build
     chiu duoc).
 15. The chia se OG (Dot 1, Ruler 10:00 28/11): moi trang truyen co du the
     og (article/title/description/url/image/site_name/locale/published_time
     + twitter:card) + anh og ton tai trong _site, la JPEG dung 1200x630,
     <= 300 KB; trang chu co og co ban (website + anh mac dinh dung 1200x630);
     anh mac dinh moi ngon ngu ton tai dung 1200x630, <= 300 KB.

Exit 0 = DAT het (cho phep day). Exit 1 = co muc truot (CHAN day).
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import unicodedata
import xml.etree.ElementTree as ET
from PIL import Image as PilImage
from pathlib import Path

EMAIL = "nguyentrungduc01092000@gmail.com"
LEGAL_RELS = ("de/impressum", "de/datenschutz", "de/kontakt",
              "pl/polityka-prywatnosci", "pl/kontakt")
SUN = "https://sunbow.click"
PLA = "https://plasma.click"
FICTION = {"de": "Alle Geschichten auf dieser Website sind frei erfunden.",
           "pl": "Wszystkie historie na tej stronie są fikcją."}
ALLOWED_EXT = {".html", ".css", ".js", ".json", ".xml", ".txt", ".svg",
               ".webp", ".avif", ".jpeg", ".jpg", ".png", ".gif", ".ico",
               ".yml", ".yaml"}  # .yml/.yaml: chi admin/config.yml (cau hinh Sveltia CMS)
ALLOWED_NAMES = {"cname"}


def nfc(s):
    return unicodedata.normalize("NFC", s)


def visible_text(html):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def resolve_cover_path(raw):
    """Duong dan cover trong front matter -> duong dan dia tuong doi goc site.
    Chap nhan ca 'src/media/...' (file doi viet) va '/media/...' (Sveltia ghi
    theo public_folder) — ca 2 deu tro toi src/media/... tren dia."""
    p = raw.strip().strip("\"'")
    if p.startswith("/"):
        p = p[1:]
    if p.startswith("media/"):
        p = "src/" + p
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site-dir", default=None)
    ap.add_argument("--expect", type=int, default=None)  # chi de doi chieu, khong bat buoc
    ap.add_argument("--expect-de", type=int, default=None)
    ap.add_argument("--expect-pl", type=int, default=None)
    ap.add_argument("--no-build", action="store_true")
    ap.add_argument("--domain", default=None)
    a = ap.parse_args()

    if a.site_dir:
        site = Path(a.site_dir).expanduser().resolve()
    else:
        site = Path(__file__).resolve().parent.parent.parent / "site"
    out = site / "_site"
    src = site / "src"
    ok = True
    # Ngon ngu dang kiem (Phuong an A, Ruler 15:52 27/11): --domain quyet dinh;
    # neu khong co --domain thi lay SITE_LANG; neu ca 2 deu khong co thi kiem
    # ban gop cu (ca 2 ngon ngu). LANG=None = ban gop.
    DOMAIN_LANG = {"sunbow.click": "de", "plasma.click": "pl"}
    if a.domain:
        if a.domain not in DOMAIN_LANG:
            print(f"--domain phai la sunbow.click hoac plasma.click (nhan {a.domain!r})")
            sys.exit(2)
        LANG = DOMAIN_LANG[a.domain]
    elif os.environ.get("SITE_LANG") in ("de", "pl"):
        LANG = os.environ["SITE_LANG"]
    else:
        LANG = None
    DOMAIN = {"de": "sunbow.click", "pl": "plasma.click"}.get(LANG)
    # So truyen ky vong: TU DEM tu file .md nguon trong repo (Ruler 28/11/2026)
    # — khong con so ghi cung: them/xoa truyen qua CMS hay them tay thi cong
    # tu cap nhat theo, khong can sua cong. --expect/--expect-de/--expect-pl
    # (neu truyen) CHI DE DOI CHIEU: khac so dem thi in ghi chu, khong truot.
    # (Rieng ngon ngu KHONG build trong che do --domain thi khong doi chieu,
    # vi --expect cua no mang nghia "build 0", khong phai so file nguon.)
    src_count = {}
    for lang in ("de", "pl"):
        posts = src / lang / "posts"
        src_count[lang] = len(list(posts.glob("*.md"))) if posts.exists() else 0
    expect = dict(src_count)
    check = {"de": a.expect_de if a.expect_de is not None else a.expect,
             "pl": a.expect_pl if a.expect_pl is not None else a.expect}
    for lang in ("de", "pl"):
        if LANG and lang != LANG:
            continue
        if check[lang] is not None and check[lang] != src_count[lang]:
            print(f"   (doi chieu: --expect-{lang}={check[lang]} khac so dem tu "
                  f"nguon={src_count[lang]} — dung so dem tu nguon)")

    def fail(msg):
        nonlocal ok
        print(f"   TRUOT: {msg}")
        ok = False

    # ---------- 0. Build ----------
    if a.no_build:
        print("0. Build: BO QUA (--no-build, dung _site hien co)")
    else:
        print("0. Build: dang chay `npm run build` (tang dan, khong xoa _site)"
              + (f" [SITE_LANG={LANG}]" if LANG else " [ban gop]") + "...")
        try:
            # (Phuong an A) Build tang dan KHONG xoa file cu trong _site, nen
            # phai xoa tay thu muc cua ngon ngu kia (neu con tu ban gop truoc)
            # truoc khi build — neu khong, trang cu cua ngon ngu kia van nam
            # trong _site va muc 13 se truot. Giu lai _site/img (cache anh).
            if LANG:
                other_lang = "pl" if LANG == "de" else "de"
                stale = out / other_lang
                if stale.exists():
                    shutil.rmtree(stale)
                    print(f"   (da xoa thu muc cu _site/{other_lang}/ cua ngon ngu kia)")
                if LANG == "pl":
                    dash = out / "dashboard"
                    if dash.exists():
                        shutil.rmtree(dash)
                        print("   (da xoa thu muc cu _site/dashboard/ — chi co tren ban de)")
            # Truyen SITE_LANG vao build de loc dung ngon ngu.
            build_env = dict(os.environ)
            if LANG:
                build_env["SITE_LANG"] = LANG
            r = subprocess.run(["npm", "run", "build"], cwd=site,
                               capture_output=True, text=True, timeout=1500,
                               env=build_env)
            tail = (r.stdout + r.stderr).strip().splitlines()[-3:]
            if r.returncode != 0:
                fail(f"npm run build exit={r.returncode}: {'; '.join(tail)}")
            else:
                print(f"   DAT (exit 0; {'; '.join(tail)})")
        except subprocess.TimeoutExpired:
            fail("npm run build qua 1500s (build sach co the ket ~10 phut o eleventy-img "
                 "— chi chay khi _site bi mat; binh thuong build tang dan vai giay)")
        except FileNotFoundError:
            fail("khong tim thay npm (can Node 24 + npm install truoc)")

    if not out.exists():
        print("KET LUAN: TRUOT - CHAN DAY (khong co _site)")
        sys.exit(1)
    htmls = sorted(out.rglob("*.html"))

    # ---------- 1. So truyen ----------
    built = {}
    for lang in ("de", "pl"):
        posts_dir = out / lang
        # trang truyen = _site/<lang>/<slug>/index.html, tru trang chu + chuyen muc + phap ly
        fixed = {"index.html", "kategorie", "kategoria", "impressum",
                 "datenschutz", "kontakt", "ueber-uns", "polityka-prywatnosci",
                 "o-nas"}
        pages = [p for p in posts_dir.glob("*/index.html")
                 if p.parent.name not in fixed]
        built[lang] = sorted(p.stem and p.parent.name for p in pages)
        src_n = len(list((src / lang / "posts").glob("*.md"))) if (src / lang / "posts").exists() else 0
        src_slugs = {p.stem for p in (src / lang / "posts").glob("*.md")} if (src / lang / "posts").exists() else set()
        missing_build = sorted(src_slugs - set(built[lang]))
        if LANG and lang != LANG:
            # (Phuong an A) Ngon ngu kia KHONG build: phai co 0 truyen da build
            # nhung file .md nguon van phai con (chung minh khong xoa khoi repo).
            if len(built[lang]) != 0 or src_n == 0:
                fail(f"{lang}: ban {LANG} khong duoc build truyen {lang} "
                     f"(da build {len(built[lang])}); .md nguon {src_n} "
                     f"(phai > 0 — file nguon phai giu trong repo)")
            else:
                print(f"1. So truyen {lang}: DAT (khong build — dung Phuong an A; "
                      f".md nguon van giu {src_n} file trong repo)")
        elif len(built[lang]) != expect[lang] or src_n != len(built[lang]):
            fail(f"{lang}: build duoc {len(built[lang])} truyen (can {expect[lang]}); "
                 f".md nguon {src_n} (khong co trang build: {missing_build or 'khong co'})")
        else:
            print(f"1. So truyen {lang}: DAT ({len(built[lang])} truyen, .md nguon khop)")

    # ---------- 2. Sitemap ----------
    sp = out / "sitemap.xml"
    story_urls = {}
    try:
        root = ET.parse(sp).getroot()
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = root.findall("s:url", ns) or root.findall("url")
        locs = []
        for u in urls:
            loc = u.find("s:loc", ns)
            if loc is None:
                loc = u.find("loc")
            if loc is not None and loc.text:
                locs.append(loc.text.strip())
        n_de = len(built.get("de", []))
        n_pl = len(built.get("pl", []))
        # (Phuong an A) Khi co --domain/SITE_LANG, sitemap chi chua URL cua
        # domain do: sunbow = truyen DE + 10, plasma = truyen PL + 8.
        # Khi khong co, ban gop cu: tong = DE + PL + 18.
        if LANG == "de":
            exp_total, exp_sun, exp_pla = n_de + 10, n_de + 10, 0
        elif LANG == "pl":
            exp_total, exp_sun, exp_pla = n_pl + 8, 0, n_pl + 8
        else:
            exp_total = n_de + n_pl + 18
            exp_sun = n_de + 10  # trang chu DE + dashboard + 4 phap ly DE + 4 chuyen muc DE
            exp_pla = n_pl + 8   # trang chu PL + 3 phap ly PL + 4 chuyen muc PL
        sun = sum(1 for l in locs if l.startswith(SUN + "/"))
        pla = sum(1 for l in locs if l.startswith(PLA + "/"))
        wrong = [l for l in locs
                 if not l.startswith(SUN + "/") and not l.startswith(PLA + "/")]
        # URL sai domain theo ngon ngu: /de/* + /dashboard/ phai o sunbow, con lai o plasma
        wrong_lang = []
        for l in locs:
            m = re.match(r"https://([^/]+)(/.*)$", l)
            if not m:
                continue
            host, path = m.group(1), m.group(2)
            exp_host = "sunbow.click" if (path.startswith("/de/") or path == "/dashboard/") else "plasma.click"
            if host != exp_host:
                wrong_lang.append(l)
        # moi URL truyen phai co trong sitemap
        missing_story = []
        for lang, base in (("de", SUN), ("pl", PLA)):
            for slug in built.get(lang, []):
                if f"{base}/{lang}/{slug}/" not in locs:
                    missing_story.append(f"{lang}/{slug}")
        if (len(locs) != exp_total or sun != exp_sun or pla != exp_pla
                or wrong or wrong_lang or missing_story):
            fail(f"sitemap: {len(locs)} loc (can {exp_total}: {exp_sun} sunbow / "
                 f"{exp_pla} plasma; thuc {sun}/{pla}); loc sai mien: {wrong}; "
                 f"loc sai domain theo ngon ngu: {wrong_lang}; truyen thieu trong "
                 f"sitemap: {missing_story}")
        else:
            print(f"2. Sitemap: DAT ({len(locs)} loc: {sun} sunbow / {pla} plasma; "
                  f"du {n_de} URL truyen DE + {n_pl} URL truyen PL)")
    except ET.ParseError as e:
        fail(f"sitemap.xml loi parse: {e}")
    except FileNotFoundError:
        fail("khong co _site/sitemap.xml")

    # ---------- 3. robots.txt ----------
    rp = out / "robots.txt"
    if not rp.exists():
        fail("khong co _site/robots.txt")
    else:
        text = rp.read_text(encoding="utf-8", errors="ignore")
        sitemaps = re.findall(r"^Sitemap:\s*(https://\S+)", text, flags=re.M)
        disallows = re.findall(r"^Disallow:\s*(.*)$", text, flags=re.M | re.I)
        bad_dis = [d for d in disallows if d.strip() not in ("/admin/", "/admin")]
        # (Phuong an A) Khi co --domain/SITE_LANG: dung 1 dong Sitemap cua
        # domain do; khi khong co: dung 2 dong [sunbow, plasma] nhu cu.
        if LANG == "de":
            exp_sitemaps = [SUN + "/sitemap.xml"]
        elif LANG == "pl":
            exp_sitemaps = [PLA + "/sitemap.xml"]
        else:
            exp_sitemaps = [SUN + "/sitemap.xml", PLA + "/sitemap.xml"]
        if (sitemaps != exp_sitemaps
                or "Allow: /" not in text or bad_dis):
            fail(f"robots: Sitemap={sitemaps} (can {exp_sitemaps}); "
                 f"Disallow={disallows} (chi duoc /admin/)")
        else:
            print(f"3. robots.txt: DAT (Allow /; chi Disallow /admin/; dung {len(exp_sitemaps)} dong Sitemap)")

    # ---------- 4. Canonical ----------
    # Trang admin noi bo (Sveltia + 2 trang cong cu Dot 1) khong co canonical
    # (khong phai trang cong khai, noindex + Disallow /admin/).
    canon_skip = {"admin/index.html", "admin/chia-se/index.html", "admin/thong-ke/index.html"}
    canon_bad = []
    n_canon_checked = 0
    for h in htmls:
        rel = str(h.relative_to(out))
        if rel in canon_skip:
            continue
        n_canon_checked += 1
        t = nfc(h.read_text(encoding="utf-8", errors="ignore"))
        ms = re.findall(r'<link rel="canonical" href="([^"]+)"', t)
        if len(ms) != 1:
            canon_bad.append(f"{rel}: {len(ms)} canonical")
            continue
        got = ms[0]
        if rel == "index.html":
            # Trang goc chuyen ve ngon ngu cua web nay (Phuong an A).
            exp = SUN + "/de/" if LANG != "pl" else PLA + "/pl/"
        else:
            url = "/" + rel[:-len("index.html")] if rel.endswith("index.html") else "/" + rel
            exp_host = "sunbow.click" if (url.startswith("/de/") or url == "/dashboard/") else "plasma.click"
            exp = f"https://{exp_host}{url}"
        if got != exp:
            canon_bad.append(f"{rel}: {got} (can {exp})")
    if n_canon_checked == 0:
        canon_bad.append("khong co trang cong khai nao de kiem (build co the da truot)")
    if canon_bad:
        fail(f"canonical sai/thieu ({len(canon_bad)} trang): {canon_bad[:5]}")
    else:
        print(f"4. Canonical: DAT ({n_canon_checked} trang cong khai, dung domain theo ngon ngu)")

    # ---------- 5. Email that ----------
    email_files = []
    for h in htmls:
        t = nfc(h.read_text(encoding="utf-8", errors="ignore"))
        if EMAIL in t:
            email_files.append(str(h.relative_to(out)))
    # (Phuong an A) Chi kiem trang phap ly cua ngon ngu do: ban de 3 trang,
    # ban pl 2 trang; ban gop thi du 5 trang nhu cu.
    if LANG == "de":
        legal_rels = ("de/impressum", "de/datenschutz", "de/kontakt")
        name_pages = ("de/impressum", "de/datenschutz")
    elif LANG == "pl":
        legal_rels = ("pl/polityka-prywatnosci", "pl/kontakt")
        name_pages = ("pl/polityka-prywatnosci",)
    else:
        legal_rels = LEGAL_RELS
        name_pages = ("de/impressum", "de/datenschutz", "pl/polityka-prywatnosci")
    email_rels = {f[:-len("/index.html")] if f.endswith("/index.html") else f
                  for f in email_files}
    email_extra = sorted(email_rels - set(legal_rels))
    email_missing = sorted(set(legal_rels) - email_rels)
    name_ok = all((out / (lr + "/index.html")).is_file()
                  and "Nguyen Trung Duc" in nfc((out / (lr + "/index.html")).read_text(encoding="utf-8", errors="ignore"))
                  for lr in name_pages)
    diacritic = [str(h.relative_to(out)) for h in htmls
                 if "Nguyễn Trung Đức" in nfc(h.read_text(encoding="utf-8", errors="ignore"))]
    ruler_hits = [str(h.relative_to(out)) for h in htmls
                  if re.search(r"\bRuler\b", visible_text(nfc(h.read_text(encoding="utf-8", errors="ignore"))))]
    if email_extra or email_missing or not name_ok or diacritic or ruler_hits:
        fail(f"email: ngoai {len(legal_rels)} trang phap ly: {email_extra}; thieu o trang phap ly: "
             f"{email_missing}; ten 'Nguyen Trung Duc' du o {len(name_pages)} trang phap ly chinh: "
             f"{'co' if name_ok else 'THIEU'}; ten co dau: {diacritic}; tu 'Ruler' "
             f"trong chu hien thi: {ruler_hits}")
    else:
        print(f"5. Email that: DAT (chi o dung {len(legal_rels)} trang phap ly; ten dung dang khong dau; "
              "0 'Nguyễn Trung Đức'; 0 tu 'Ruler')")

    # ---------- 6. AdSense BAT ----------
    pub = "ca-pub-1934454305970765"
    # Trang khong dung base.njk: chuyen huong goc + CMS admin + 2 trang cong cu
    # admin noi bo (Dot 1) — khong co ma AdSense.
    html_no_code = {"index.html", "admin/index.html",
                    "admin/chia-se/index.html", "admin/thong-ke/index.html"}
    bad_code = []
    for h in htmls:
        rel = str(h.relative_to(out))
        n = h.read_text(encoding="utf-8", errors="ignore").count(pub)
        want = 0 if rel in html_no_code else 1
        if n != want:
            bad_code.append(f"{rel}: {n} (can {want})")
    non_html_hits = []
    for f in sorted(out.rglob("*")):
        if not f.is_file() or f.suffix.lower() == ".html":
            continue
        try:
            t = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if pub in t or "adsbygoogle" in t:
            non_html_hits.append(str(f.relative_to(out)))
    ads_txt_f = (out / "ads.txt")
    ads_txt_ok = ads_txt_f.exists() and ads_txt_f.read_text(encoding="utf-8").strip() == "google.com, pub-1934454305970765, DIRECT, f08c47fec0942fa0"
    gfile = list(out.glob("google*.html"))
    if bad_code or non_html_hits or not ads_txt_ok or gfile:
        fail(f"AdSense: HTML sai so ma: {bad_code}; file khong-phai-HTML chua ma: {non_html_hits}; "
             f"ads.txt: {'DAT' if ads_txt_ok else 'SAI/thieu'}; "
             f"file xac minh google*.html: {[str(p.relative_to(out)) for p in gfile]}")
    else:
        print("6. AdSense BAT: DAT (moi HTML dung base.njk dung 1 ma; admin + trang chuyen huong 0 ma; ads.txt dung; khong file google*.html)")

    # ---------- 7. Giu cho + repo admin ----------
    ph_files = []
    for h in htmls:
        t = nfc(h.read_text(encoding="utf-8", errors="ignore"))
        if "GIỮ CHỖ" in visible_text(t):
            ph_files.append(str(h.relative_to(out)))
    sm_ph = "GIỮ CHỖ" in (sp.read_text(encoding="utf-8", errors="ignore") if sp.exists() else "")
    rb_ph = "GIỮ CHỖ" in (rp.read_text(encoding="utf-8", errors="ignore") if rp.exists() else "")
    cfg_src = src / "admin/config.yml"
    cfg_out = out / "admin/config.yml"
    cfg_bad = []
    for cfg in (cfg_src, cfg_out):
        if not cfg.exists():
            cfg_bad.append(f"{cfg} (khong co)")
        else:
            ct = cfg.read_text(encoding="utf-8", errors="ignore")
            if "GIỮ CHỖ" in ct:
                cfg_bad.append(f"{cfg} (repo con giu cho)")
            elif not re.search(r'repo:\s*"?[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+"?', ct):
                cfg_bad.append(f"{cfg} (repo khong dung dang owner/repo)")
    if ph_files or sm_ph or rb_ph or cfg_bad:
        fail(f"giu cho: trong chu hien thi HTML: {ph_files}; sitemap/robots: "
             f"{'CO' if (sm_ph or rb_ph) else 'khong'}; admin config.yml: {cfg_bad}")
    else:
        print("7. Giu cho: DAT (0 '[GIỮ CHỖ]' trong chu hien thi/sitemap/robots; "
              "repo admin la owner/repo that)")

    # ---------- 8. Allowlist ----------
    bad_files = []
    for f in sorted(out.rglob("*")):
        if not f.is_file():
            continue
        rel = f.relative_to(out)
        if f.suffix.lower() in ALLOWED_EXT or f.name.lower() in ALLOWED_NAMES:
            continue
        bad_files.append(f"{rel} (loai khong duoc phep: {f.suffix or 'khong co duoi'})")
    if bad_files:
        fail(f"allowlist ({len(bad_files)} file): {bad_files[:5]}")
    else:
        print("8. Allowlist: DAT (tat ca file trong _site deu thuoc danh sach cho phep)")

    # ---------- 9. CNAME / workflow ----------
    cname = site / "CNAME"
    cname_bad = []
    if not cname.exists():
        cname_bad.append("khong co file CNAME o goc repo")
    else:
        dom = cname.read_text(encoding="utf-8", errors="ignore").strip()
        if dom not in ("sunbow.click", "plasma.click"):
            cname_bad.append(f"CNAME chua '{dom}' (phai la sunbow.click hoac plasma.click)")
        elif a.domain and dom != a.domain:
            cname_bad.append(f"CNAME '{dom}' khac --domain {a.domain}")
    # (Phuong an A) Ca 2 workflow phai co: copy CNAME + kiem chung
    # sitemap/robots theo domain + dat SITE_LANG theo CNAME (neu khong,
    # rebuild dinh ky se dua ban gop len live lai).
    wf_files = [site / ".github/workflows/deploy-pages.yml",
                site / ".github/workflows/scheduled-build.yml"]
    wf_bad = []
    for wf in wf_files:
        if not wf.exists():
            wf_bad.append(f"khong co {wf.relative_to(site)}")
            continue
        wf_text = wf.read_text(encoding="utf-8", errors="ignore")
        wname = str(wf.relative_to(site))
        if "cp CNAME _site/CNAME" not in wf_text:
            wf_bad.append(f"{wname}: khong co buoc copy CNAME vao _site")
        if "split-sitemap-robots" not in wf_text:
            wf_bad.append(f"{wname}: khong co buoc kiem chung sitemap/robots theo domain")
        if "SITE_LANG" not in wf_text:
            wf_bad.append(f"{wname}: khong co buoc dat SITE_LANG theo CNAME")
    if cname_bad or wf_bad:
        fail(f"CNAME/workflow: {cname_bad}; {wf_bad}")
    else:
        dom = cname.read_text(encoding="utf-8", errors="ignore").strip()
        print(f"9. CNAME/workflow: DAT (CNAME={dom}; 2 workflow co buoc copy CNAME + kiem chung sitemap/robots + SITE_LANG)")

    # ---------- 10. Cau hu cau ----------
    fic_bad = []
    for lang in ("de", "pl"):
        home = out / lang / "index.html"
        if home.exists() and FICTION[lang] not in nfc(home.read_text(encoding="utf-8", errors="ignore")):
            fic_bad.append(f"{lang}/ (trang chu thieu cau hu cau)")
        for slug in built.get(lang, []):
            p = out / lang / slug / "index.html"
            if not p.exists() or FICTION[lang] not in nfc(p.read_text(encoding="utf-8", errors="ignore")):
                fic_bad.append(f"{lang}/{slug}")
    if fic_bad:
        fail(f"cau hu cau thieu o: {fic_bad}")
    else:
        # So trang chu that su da kiem (ban theo domain chi co 1 trang chu).
        n_home = sum(1 for lang in ("de", "pl") if (out / lang / "index.html").exists())
        print(f"10. Cau hu cau: DAT (du tren {len(built.get('de', [])) + len(built.get('pl', []))} trang truyen + {n_home} trang chu)")

    # ---------- 11. Anh bia: moi the co anh tai duoc ----------
    # (Ruler 07:41 ngay 27/11: demo tach anh ra assets lam anh Duc chi thay
    #  alt. Muc nay dam bao moi truyen co file anh bia that o dung duong dan
    #  front matter, va moi <img> tren trang chu + trang danh muc + trang
    #  truyen deu tro toi file that trong _site, kich thuoc > 0.)
    import re as _re
    img_bad = []
    for lang in ("de", "pl"):
        for md in sorted((src / lang / "posts").glob("*.md")):
            m = _re.search(r"^cover:\s*[\"']?(.*?)[\"']?\s*$",
                           md.read_text(encoding="utf-8", errors="ignore"), _re.M)
            if not m:
                img_bad.append(f"{lang}/{md.stem}: khong co truong cover")
                continue
            f = site / resolve_cover_path(m.group(1))
            if not f.is_file():
                img_bad.append(f"{lang}/{md.stem}: cover khong co file {m.group(1)}")
            elif f.stat().st_size == 0:
                img_bad.append(f"{lang}/{md.stem}: cover rong 0B {m.group(1)}")
    list_pages = [out / "de" / "index.html", out / "pl" / "index.html"]
    list_pages += sorted((out / "de" / "kategorie").glob("*/index.html"))
    list_pages += sorted((out / "pl" / "kategoria").glob("*/index.html"))
    for lang in ("de", "pl"):
        for slug in built.get(lang, []):
            list_pages.append(out / lang / slug / "index.html")
    seen = set()
    for pg in list_pages:
        if not pg.exists():
            continue
        for s in _re.findall(r'<img[^>]+src="([^"]+)"',
                             pg.read_text(encoding="utf-8", errors="ignore")):
            p = s.split("?")[0]
            if p.startswith("data:") or p in seen:
                continue
            seen.add(p)
            f = out / p.lstrip("/")
            if not f.is_file():
                img_bad.append(f"{pg.relative_to(out)}: img khong co file {p}")
            elif f.stat().st_size == 0:
                img_bad.append(f"{pg.relative_to(out)}: img rong 0B {p}")
    if img_bad:
        fail("anh bia loi: " + "; ".join(img_bad[:10])
             + (f" (+{len(img_bad) - 10} loi nua)" if len(img_bad) > 10 else ""))
    else:
        n_story = len(built.get("de", [])) + len(built.get("pl", []))
        print(f"11. Anh bia: DAT ({n_story} truyen co cover that; {len(seen)} img "
              f"tren trang chu/danh muc/truyen deu ton tai, >0B)")

    # ---------- 12. Admin sach: khong ghi chu noi bo tren live ----------
    # (Ruler 11:50 27/11: config.yml live lo 48 dong binh luan tieng Viet.
    #  Buoc dung strip-admin-config.js bo dong # khi build; muc nay kiem
    #  lai tren _site.)
    admin_dir = out / "admin"
    admin_bad = []
    if not admin_dir.exists():
        admin_bad.append("thieu thu muc _site/admin/")
    else:
        for f in sorted(admin_dir.rglob("*")):
            if not f.is_file():
                continue
            rel = str(f.relative_to(out))
            try:
                lines = f.read_text(encoding="utf-8", errors="ignore").splitlines()
            except OSError:
                continue
            n_hash = sum(1 for ln in lines if ln.lstrip().startswith("#"))
            if n_hash:
                admin_bad.append(f"{rel}: {n_hash} dong bat dau bang #")
            t = "\n".join(lines)
            if "<!--" in t:
                admin_bad.append(f"{rel}: chua chu thich HTML <!-- -->")
            for w in ("Ruler", "GIỮ CHỖ"):
                if w in t:
                    admin_bad.append(f"{rel}: chua tu '{w}'")
    admin_idx = admin_dir / "index.html"
    if admin_idx.exists() and "noindex" not in admin_idx.read_text(encoding="utf-8", errors="ignore").lower():
        admin_bad.append("admin/index.html thieu meta noindex")
    if admin_bad:
        fail(f"admin sach: {admin_bad}")
    else:
        print("12. Admin sach: DAT (0 dong # + 0 chu thich HTML + 0 tu noi bo trong _site/admin/; admin co noindex)")

    # ---------- 13. Mot ngon ngu moi web (Phuong an A) ----------
    # Chi chay khi co --domain hoac SITE_LANG (LANG is not None). Khi khong
    # co, ban gop la hanh vi cu nen bo qua.
    if LANG is None:
        print("13. Mot ngon ngu: BO QUA (khong co --domain/SITE_LANG — kiem ban gop)")
    else:
        other_lang = "pl" if LANG == "de" else "de"
        other_dom = "plasma.click" if LANG == "de" else "sunbow.click"
        dom_url = SUN if LANG == "de" else PLA
        one_bad = []
        # (a) Khong co thu muc/trang cua ngon ngu kia trong _site
        other_dir = out / other_lang
        if other_dir.exists() and any(other_dir.rglob("*")):
            one_bad.append(f"con thu muc _site/{other_lang}/ (ngon ngu kia)")
        if LANG == "pl":
            dash = out / "dashboard"
            if dash.exists() and any(dash.rglob("*")):
                one_bad.append("con thu muc _site/dashboard/ (chi co tren ban de)")
        # (b) 0 link noi bo toi ngon ngu kia + 0 chuoi domain kia + 0 nut
        # chuyen ngon ngu trong HTML da dung
        href_re = re.compile(r'href="([^"]+)"')
        for h in htmls:
            rel = str(h.relative_to(out))
            t = nfc(h.read_text(encoding="utf-8", errors="ignore"))
            if "lang-switch" in t:
                one_bad.append(f"{rel}: con nut chuyen ngon ngu (lang-switch)")
                continue
            if other_dom in t:
                one_bad.append(f"{rel}: chua chuoi domain kia {other_dom}")
                continue
            bad_href = [u for u in href_re.findall(t)
                        if u.startswith(f"/{other_lang}/")
                        or u.startswith(f"https://{other_dom}/")]
            if bad_href:
                one_bad.append(f"{rel}: link toi ngon ngu kia: {bad_href[:3]}")
        # (c) Canonical moi trang tu tro ve domain dang kiem
        canon_other = []
        for h in htmls:
            rel = str(h.relative_to(out))
            if rel == "admin/index.html":
                continue
            t = nfc(h.read_text(encoding="utf-8", errors="ignore"))
            ms = re.findall(r'<link rel="canonical" href="([^"]+)"', t)
            if len(ms) == 1 and not ms[0].startswith(dom_url + "/"):
                canon_other.append(f"{rel}: {ms[0]}")
        if canon_other:
            one_bad.append(f"canonical khong tu tro ve {DOMAIN}: {canon_other[:3]}")
        # (d) Admin da dung chi co collection posts cua ngon ngu do + du
        # About/Legal cua ngon ngu do; config nguon van du ca 2 collection
        cfg_out_text = cfg_out.read_text(encoding="utf-8", errors="ignore") if cfg_out.exists() else ""
        cfg_src_text = cfg_src.read_text(encoding="utf-8", errors="ignore") if cfg_src.exists() else ""
        if f"  - name: posts_{LANG}" not in cfg_out_text:
            one_bad.append(f"_site/admin/config.yml thieu collection posts_{LANG}")
        if f"  - name: posts_{other_lang}" in cfg_out_text:
            one_bad.append(f"_site/admin/config.yml con collection posts_{other_lang}")
        for coll in ("about", "legal"):
            if f"  - name: {coll}" not in cfg_out_text:
                one_bad.append(f"_site/admin/config.yml thieu collection {coll}")
        if LANG == "de":
            want_files = ("ueber_uns", "impressum", "datenschutz", "kontakt_de")
            ban_files = ("o_nas", "polityka", "kontakt")
        else:
            want_files = ("o_nas", "polityka", "kontakt")
            ban_files = ("ueber_uns", "impressum", "datenschutz", "kontakt_de")
        # (Dung regex neo dau/cuoi dong: "kontakt" la tien to cua "kontakt_de"
        # nen kiem chuoi con se bao sai.)
        for fname in want_files:
            if not re.search(rf"^      - name: {re.escape(fname)}\s*$", cfg_out_text, flags=re.M):
                one_bad.append(f"_site/admin/config.yml thieu muc file {fname}")
        for fname in ban_files:
            if re.search(rf"^      - name: {re.escape(fname)}\s*$", cfg_out_text, flags=re.M):
                one_bad.append(f"_site/admin/config.yml con muc file {fname} (ngon ngu kia)")
        # (e) Menu: chi giu truong menu cua ngon ngu do trong file menus
        # (Ruler 11:20 28/11 — #07 live tung con pl_header/pl_footer).
        if LANG == "de":
            want_menu = ("de_header", "de_footer")
            ban_menu = ("pl_header", "pl_footer")
        else:
            want_menu = ("pl_header", "pl_footer")
            ban_menu = ("de_header", "de_footer")
        for mname in want_menu:
            if not re.search(rf"^          - name: {re.escape(mname)}\s*$", cfg_out_text, flags=re.M):
                one_bad.append(f"_site/admin/config.yml thieu truong menu {mname}")
        for mname in ban_menu:
            if re.search(rf"^          - name: {re.escape(mname)}\s*$", cfg_out_text, flags=re.M):
                one_bad.append(f"_site/admin/config.yml con truong menu {mname} (ngon ngu kia)")
        if (f"  - name: posts_{LANG}" not in cfg_src_text
                or f"  - name: posts_{other_lang}" not in cfg_src_text):
            one_bad.append("src/admin/config.yml thieu 1 trong 2 collection posts (nguon phai giu du ca 2)")
        if one_bad:
            fail(f"mot ngon ngu: {one_bad[:8]}"
                 + (f" (+{len(one_bad) - 8} loi nua)" if len(one_bad) > 8 else ""))
        else:
            print(f"13. Mot ngon ngu: DAT (0 trang {other_lang} trong _site; 0 link cheo; "
                  f"canonical tu tro ve {DOMAIN}; admin chi posts_{LANG}; menu chi {LANG})")

    # ---------- 14. Front matter cua file do CMS tao ----------
    # (Ruler 10:14 28/11 — Sveltia tung ghi sai dinh dang ban build cho:
    # date co gio, thieu tags, cover dang /media/, permalink /de//. Bay gio
    # config da sua + build da chiu duoc — muc nay bat file nao van sai
    # truoc khi day.)
    fm_bad = []

    def _fm_field(fm_text, name):
        m = re.search(rf"^{name}:\s*(.+?)\s*$", fm_text, flags=re.M)
        return m.group(1).strip() if m else None

    for lang in ("de", "pl"):
        for md in sorted((src / lang / "posts").glob("*.md")):
            text = md.read_text(encoding="utf-8", errors="ignore")
            m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.S)
            if not m:
                fm_bad.append(f"{lang}/{md.stem}: khong co khoi front matter ---")
                continue
            fm = m.group(1)
            errs = []
            date_v = _fm_field(fm, "date")
            if date_v is None:
                errs.append("thieu date")
            elif not re.match(r"^\d{4}-\d{2}-\d{2}$", date_v.strip("\"'")):
                errs.append(f"date sai dang (phai YYYY-MM-DD, khong gio): {date_v}")
            slug_v = _fm_field(fm, "slug")
            slug_c = slug_v.strip("\"'") if slug_v else None
            if slug_v is None:
                errs.append("thieu slug")
            elif not re.match(r"^[a-z0-9-]+$", slug_c):
                errs.append(f"slug sai dang: {slug_v}")
            cover_v = _fm_field(fm, "cover")
            if cover_v is None:
                errs.append("thieu cover")
            else:
                cf = site / resolve_cover_path(cover_v)
                if not cf.is_file():
                    errs.append(f"cover khong co file: {cover_v}")
                elif cf.stat().st_size == 0:
                    errs.append(f"cover rong 0B: {cover_v}")
            perm_v = _fm_field(fm, "permalink")
            if perm_v is not None and slug_c is not None:
                pv = perm_v.strip("\"'")
                ok_perm = ("/" + lang + "/" + slug_c + "/",
                           "/" + lang + "/{{ slug }}/")
                if pv not in ok_perm:
                    errs.append("permalink sai: " + pv + " (phai /" + lang + "/"
                                + slug_c + "/ hoac /" + lang + "/{{ slug }}/ hoac khong co)")
            layout_v = _fm_field(fm, "layout")
            if layout_v is not None and layout_v.strip("\"'") != "layouts/post.njk":
                errs.append(f"layout sai: {layout_v}")
            tags_m = re.search(r"^tags:\s*(.*)$", fm, flags=re.M)
            if tags_m is not None:
                tv = tags_m.group(1).strip()
                if tv == "":
                    after = fm[tags_m.end():]
                    if not re.search(r"^\s*-\s+\S", after, flags=re.M):
                        errs.append("tags rong (khong phai list)")
                elif not re.match(r"^\[.*\]$", tv):
                    errs.append(f"tags khong phai list: {tv}")
            if errs:
                fm_bad.append(f"{lang}/{md.stem}: " + "; ".join(errs))
    if fm_bad:
        fail(f"front matter ({len(fm_bad)} file): " + "; ".join(fm_bad[:8])
             + (f" (+{len(fm_bad) - 8} file nua)" if len(fm_bad) > 8 else ""))
    else:
        n_posts = sum(1 for lang in ("de", "pl")
                      for _ in (src / lang / "posts").glob("*.md"))
        print(f"14. Front matter: DAT ({n_posts} bai: date chi ngay, slug hop le, "
              "cover tro file that, permalink dung/thieu, layout dung, tags list/thieu)")

    # ---------- 15. The chia se OG (Dot 1, Ruler 10:00 28/11) ----------
    # Moi trang truyen: du the og + anh og ton tai trong _site, la JPEG dung
    # 1200x630, <= 300 KB. Trang chu: og co ban (website + anh mac dinh).
    og_bad = []

    def _og_img_ok(url, page_rel):
        # url tuyet doi https://<domain>/img/og/<ten>.jpg -> file trong _site.
        m = re.match(r"^https://(?:sunbow|plasma)\.click(/img/og/[^\"' ]+\.jpg)$", url or "")
        if not m:
            return f"{page_rel}: og:image sai dang: {url}"
        f = out / m.group(1).lstrip("/")
        if not f.is_file():
            return f"{page_rel}: og:image khong co file: {url}"
        try:
            with PilImage.open(f) as im:
                if im.size != (1200, 630) or im.format != "JPEG":
                    return f"{page_rel}: og:image sai ({im.format} {im.size[0]}x{im.size[1]}): {url}"
        except Exception as e:
            return f"{page_rel}: og:image khong doc duoc: {e}"
        if f.stat().st_size > 300 * 1024:
            return f"{page_rel}: og:image vuot 300 KB ({f.stat().st_size // 1024} KB)"
        return None

    def _og_meta(t):
        d = {}
        for k in ("og:type", "og:title", "og:description", "og:url", "og:image",
                  "og:site_name", "og:locale", "article:published_time"):
            m = re.search(rf'<meta property="{re.escape(k)}" content="([^"]*)"', t)
            if m:
                d[k] = m.group(1)
        m = re.search(r'<meta name="twitter:card" content="([^"]*)"', t)
        if m:
            d["twitter:card"] = m.group(1)
        return d

    # Anh mac dinh moi ngon ngu (ban theo domain chi can 1; ban gop can ca 2).
    for lang in ("de", "pl"):
        if LANG is not None and lang != LANG:
            continue
        d = out / "img" / "og" / f"default-{lang}.jpg"
        if not d.is_file():
            og_bad.append(f"thieu anh mac dinh img/og/default-{lang}.jpg")
            continue
        try:
            with PilImage.open(d) as im:
                if im.size != (1200, 630) or im.format != "JPEG":
                    og_bad.append(f"default-{lang}.jpg sai ({im.format} {im.size[0]}x{im.size[1]})")
        except Exception as e:
            og_bad.append(f"default-{lang}.jpg khong doc duoc: {e}")
        if d.stat().st_size > 300 * 1024:
            og_bad.append(f"default-{lang}.jpg vuot 300 KB ({d.stat().st_size // 1024} KB)")
    # Trang truyen: du the og + anh dung 1200x630.
    for lang in ("de", "pl"):
        for slug in built.get(lang, []):
            p = out / lang / slug / "index.html"
            rel = f"{lang}/{slug}"
            if not p.exists():
                og_bad.append(f"{rel}: thieu trang")
                continue
            t = nfc(p.read_text(encoding="utf-8", errors="ignore"))
            meta = _og_meta(t)
            for k in ("og:type", "og:title", "og:description", "og:url", "og:image",
                      "og:site_name", "og:locale", "article:published_time", "twitter:card"):
                if k not in meta:
                    og_bad.append(f"{rel}: thieu the {k}")
            if meta.get("og:type") != "article":
                og_bad.append(f"{rel}: og:type != article ({meta.get('og:type')})")
            if meta.get("og:locale") != ("de_DE" if lang == "de" else "pl_PL"):
                og_bad.append(f"{rel}: og:locale sai ({meta.get('og:locale')})")
            if meta.get("twitter:card") != "summary_large_image":
                og_bad.append(f"{rel}: twitter:card sai ({meta.get('twitter:card')})")
            dom = SUN if lang == "de" else PLA
            if meta.get("og:url") != f"{dom}/{lang}/{slug}/":
                og_bad.append(f"{rel}: og:url sai ({meta.get('og:url')})")
            if "og:image" in meta:
                err = _og_img_ok(meta["og:image"], rel)
                if err:
                    og_bad.append(err)
    # Trang chu: og co ban (website + anh mac dinh dung 1200x630).
    for lang in ("de", "pl"):
        home = out / lang / "index.html"
        if not home.exists():
            continue
        t = nfc(home.read_text(encoding="utf-8", errors="ignore"))
        meta = _og_meta(t)
        if meta.get("og:type") != "website":
            og_bad.append(f"{lang}/ (trang chu): og:type != website ({meta.get('og:type')})")
        if "og:image" not in meta:
            og_bad.append(f"{lang}/ (trang chu): thieu og:image")
        else:
            err = _og_img_ok(meta["og:image"], f"{lang}/ (trang chu)")
            if err:
                og_bad.append(err)
    if og_bad:
        fail(f"the chia se OG ({len(og_bad)} loi): " + "; ".join(og_bad[:8])
             + (f" (+{len(og_bad) - 8} loi nua)" if len(og_bad) > 8 else ""))
    else:
        n_story = len(built.get("de", [])) + len(built.get("pl", []))
        print(f"15. The chia se OG: DAT ({n_story} trang truyen co og article + anh 1200x630; "
              "trang chu co og co ban)")

    print("KET LUAN:", "DAT - CHO PHEP DAY" if ok else "TRUOT - CHAN DAY")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
