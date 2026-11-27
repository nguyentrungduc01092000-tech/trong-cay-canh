#!/usr/bin/env python3
"""Kiem tra TRUOC KHI DAY cho 2 web truyen DE/PL (sunbow.click / plasma.click).
Nhom D, 26/11/2026 — CHUA day, chi chuan bi.

Usage:
  pre-push-check-truyen.py [--site-dir PATH] [--expect N] [--no-build] [--domain DOMAIN]
    --site-dir : thu muc site/ (mac dinh: ../site ke tu file script)
    --expect   : so truyen ky vong MOI web (mac dinh 20; demo hien tai dung 7)
    --no-build : bo qua buoc build (dung khi _site vua build xong va src/ chua doi)
    --domain   : kiem them file CNAME cua repo nay (sunbow.click hoac plasma.click)

Kiem (moi muc DAT moi cho phep day; 1 muc TRUOT = CHAN day):
  0. Build: npm run build exit 0 (build tang dan, KHONG rm -rf _site).
  1. So truyen: moi web du --expect truyen da build; file .md nguon khop so truyen
     da build (truyen nhap/hen gio chua len se bi neu ten); moi URL truyen co
     trong sitemap.
  2. Sitemap: XML hop le; tong loc = truyen DE + truyen PL + 18 trang co dinh
     (2 trang chu + dashboard + 7 phap ly/gioi thieu + 8 chuyen muc);
     sunbow = truyen DE + 10, plasma = truyen PL + 8; URL nao sai domain thi truot.
  3. robots.txt: Allow /; chi Disallow /admin/; dung 2 dong Sitemap theo thu tu
     [sunbow, plasma]; khong chan bot quang cao/Googlebot.
  4. Canonical: moi file HTML (tru admin/index.html) co dung 1 canonical
     tuyet doi, dung domain theo ngon ngu (/de/* + /dashboard/ -> sunbow,
     /pl/* -> plasma, trang goc / -> https://sunbow.click/de/); khong co
     canonical tro github.io/localhost/domain khac.
  5. Email that: nguyentrungduc01092000@gmail.com CHI o 5 trang phap ly
     (de/impressum, de/datenschutz, de/kontakt, pl/kontakt,
     pl/polityka-prywatnosci) va du ca 5 trang; ten "Nguyen Trung Duc" (khong
     dau) du o Impressum/Datenschutz/Polityka; "Nguyễn Trung Đức" (co dau) = 0;
     tu "Ruler" = 0 trong chu hien thi (quyet Ruler 14:00/14:02/14:08).
  6. AdSense BAT (Ruler 11:42 27/11): moi HTML dung base.njk dung 1 lan
     "ca-pub-1934454305970765"; admin/index.html + index.html (trang chuyen
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
     dung 1 domain; .github/workflows/deploy-pages.yml phai co buoc copy CNAME
     VA buoc tach sitemap/robots theo domain (split-sitemap-robots — Ruler
     08:50 27/11: moi domain chi co sitemap/robots cua chinh no).
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

Exit 0 = DAT het (cho phep day). Exit 1 = co muc truot (CHAN day).
"""
import argparse
import re
import subprocess
import sys
import unicodedata
import xml.etree.ElementTree as ET
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site-dir", default=None)
    ap.add_argument("--expect", type=int, default=20)
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
    expect = {"de": a.expect_de if a.expect_de is not None else a.expect,
              "pl": a.expect_pl if a.expect_pl is not None else a.expect}

    def fail(msg):
        nonlocal ok
        print(f"   TRUOT: {msg}")
        ok = False

    # ---------- 0. Build ----------
    if a.no_build:
        print("0. Build: BO QUA (--no-build, dung _site hien co)")
    else:
        print("0. Build: dang chay `npm run build` (tang dan, khong xoa _site)...")
        try:
            r = subprocess.run(["npm", "run", "build"], cwd=site,
                               capture_output=True, text=True, timeout=1500)
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
        if len(built[lang]) != expect[lang] or src_n != len(built[lang]):
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
        if (sitemaps != [SUN + "/sitemap.xml", PLA + "/sitemap.xml"]
                or "Allow: /" not in text or bad_dis):
            fail(f"robots: Sitemap={sitemaps} (can {[SUN + '/sitemap.xml', PLA + '/sitemap.xml']}); "
                 f"Disallow={disallows} (chi duoc /admin/)")
        else:
            print("3. robots.txt: DAT (Allow /; chi Disallow /admin/; dung 2 dong Sitemap)")

    # ---------- 4. Canonical ----------
    canon_bad = []
    for h in htmls:
        rel = str(h.relative_to(out))
        if rel == "admin/index.html":
            continue
        t = nfc(h.read_text(encoding="utf-8", errors="ignore"))
        ms = re.findall(r'<link rel="canonical" href="([^"]+)"', t)
        if len(ms) != 1:
            canon_bad.append(f"{rel}: {len(ms)} canonical")
            continue
        got = ms[0]
        if rel == "index.html":
            exp = SUN + "/de/"
        else:
            url = "/" + rel[:-len("index.html")] if rel.endswith("index.html") else "/" + rel
            exp_host = "sunbow.click" if (url.startswith("/de/") or url == "/dashboard/") else "plasma.click"
            exp = f"https://{exp_host}{url}"
        if got != exp:
            canon_bad.append(f"{rel}: {got} (can {exp})")
    if canon_bad:
        fail(f"canonical sai/thieu ({len(canon_bad)} trang): {canon_bad[:5]}")
    else:
        print(f"4. Canonical: DAT ({len(htmls) - 1} trang cong khai, dung domain theo ngon ngu)")

    # ---------- 5. Email that ----------
    email_files = []
    for h in htmls:
        t = nfc(h.read_text(encoding="utf-8", errors="ignore"))
        if EMAIL in t:
            email_files.append(str(h.relative_to(out)))
    email_rels = {f[:-len("/index.html")] if f.endswith("/index.html") else f
                  for f in email_files}
    email_extra = sorted(email_rels - set(LEGAL_RELS))
    email_missing = sorted(set(LEGAL_RELS) - email_rels)
    name_ok = all(EMAIL in "" or "Nguyen Trung Duc" in nfc((out / (lr + "/index.html")).read_text(encoding="utf-8", errors="ignore"))
                  for lr in ("de/impressum", "de/datenschutz", "pl/polityka-prywatnosci"))
    diacritic = [str(h.relative_to(out)) for h in htmls
                 if "Nguyễn Trung Đức" in nfc(h.read_text(encoding="utf-8", errors="ignore"))]
    ruler_hits = [str(h.relative_to(out)) for h in htmls
                  if re.search(r"\bRuler\b", visible_text(nfc(h.read_text(encoding="utf-8", errors="ignore"))))]
    if email_extra or email_missing or not name_ok or diacritic or ruler_hits:
        fail(f"email: ngoai 5 trang phap ly: {email_extra}; thieu o trang phap ly: "
             f"{email_missing}; ten 'Nguyen Trung Duc' du o 3 trang phap ly chinh: "
             f"{'co' if name_ok else 'THIEU'}; ten co dau: {diacritic}; tu 'Ruler' "
             f"trong chu hien thi: {ruler_hits}")
    else:
        print("5. Email that: DAT (chi o dung 5 trang phap ly; ten dung dang khong dau; "
              "0 'Nguyễn Trung Đức'; 0 tu 'Ruler')")

    # ---------- 6. AdSense BAT ----------
    pub = "ca-pub-1934454305970765"
    html_no_code = {"index.html", "admin/index.html"}  # trang chuyen huong goc + CMS admin khong dung base.njk
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
    wf = site / ".github/workflows/deploy-pages.yml"
    cname_bad = []
    if not cname.exists():
        cname_bad.append("khong co file CNAME o goc repo")
    else:
        dom = cname.read_text(encoding="utf-8", errors="ignore").strip()
        if dom not in ("sunbow.click", "plasma.click"):
            cname_bad.append(f"CNAME chua '{dom}' (phai la sunbow.click hoac plasma.click)")
        elif a.domain and dom != a.domain:
            cname_bad.append(f"CNAME '{dom}' khac --domain {a.domain}")
    wf_bad = []
    if not wf.exists():
        wf_bad.append("khong co .github/workflows/deploy-pages.yml")
    else:
        wf_text = wf.read_text(encoding="utf-8", errors="ignore")
        if "CNAME" not in wf_text:
            wf_bad.append("workflow khong co buoc copy CNAME vao _site")
        if "split-sitemap-robots" not in wf_text:
            wf_bad.append("workflow khong co buoc tach sitemap/robots theo domain")
    if cname_bad or wf_bad:
        fail(f"CNAME/workflow: {cname_bad}; {wf_bad}")
    else:
        dom = cname.read_text(encoding="utf-8", errors="ignore").strip()
        print(f"9. CNAME/workflow: DAT (CNAME={dom}; workflow co buoc copy CNAME + tach sitemap/robots)")

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
        print(f"10. Cau hu cau: DAT (du tren {len(built.get('de', [])) + len(built.get('pl', []))} trang truyen + 2 trang chu)")

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
            f = site / m.group(1)
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

    print("KET LUAN:", "DAT - CHO PHEP DAY" if ok else "TRUOT - CHAN DAY")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
