#!/usr/bin/env python3
"""Kiem chung + loc sitemap.xml + robots.txt theo ten mien (moi domain 1
sitemap/robots rieng).

Ly do (Ruler 08:50 27/11/2026): sitemap.xml cua sunbow.click chua 57 muc
(30 sunbow + 27 plasma) va robots.txt khai ca 2 dong Sitemap — Google xem
sitemap chua URL ten mien khac la loi, lai lo lien ket giua 2 web. Moi
domain chi duoc liet ke URL cua chinh no.

Phuong an A (Ruler 15:52 27/11/2026): build da loc theo ngon ngu
(SITE_LANG=de|pl) nen sitemap/robots sinh ra DA theo domain — script nay
chuyen thanh che do KIEM CHUNG: chap nhan sitemap da tach san (khong con
muc nao de bo la binh thuong, KHONG loi); chi khi build gop (con muc cua
domain kia) moi loc bo — luoi an toan cuoi. Kiem lai thanh pham o cuoi
dam bao khong con URL/dong Sitemap cua domain kia.

Dung o 2 cho (ca 2 deu SAU khi build xong):
  - CI: deploy-pages.yml (sau gate — gate kiem ban theo domain) va
    scheduled-build.yml (sau buoc Copy CNAME), truoc khi upload artifact.
    Domain lay tu file CNAME o goc repo.
  - Push script local: chay kiem chung tren _site cua work dir sau khi gate
    dat (khong commit — _site nam trong .gitignore; ban that tach o CI).

Chi loc 2 file trong _site, KHONG doi template nguon. Loi thi exit != 0.
"""
import argparse
import re
import sys
from pathlib import Path

DOMAINS = ("sunbow.click", "plasma.click")


def fail(msg):
    print(f"split-sitemap: LOI — {msg}")
    return 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site-dir", default=".",
                    help="goc site/repo (chua _site/; mac dinh: .)")
    ap.add_argument("--domain", default=None,
                    help="vd sunbow.click; mac dinh doc tu file CNAME")
    a = ap.parse_args()
    site = Path(a.site_dir)
    dom = a.domain
    if not dom:
        for cand in (site / "CNAME", site / "_site" / "CNAME"):
            if cand.exists():
                dom = cand.read_text(encoding="utf-8").strip()
                break
    if dom not in DOMAINS:
        return fail(f"domain khong hop le: {dom!r} (can sunbow.click|plasma.click)")
    other = DOMAINS[1] if dom == DOMAINS[0] else DOMAINS[0]
    base = f"https://{dom}"
    out = site / "_site"
    sm = out / "sitemap.xml"
    rb = out / "robots.txt"
    if not sm.exists():
        return fail("khong co _site/sitemap.xml")
    if not rb.exists():
        return fail("khong co _site/robots.txt")

    # --- sitemap.xml: chi giu <url> co <loc> thuoc domain nay ---
    text = sm.read_text(encoding="utf-8")
    m_head = re.search(r"^(.*?<urlset[^>]*>)\s*", text, flags=re.S)
    m_tail = re.search(r"</urlset>\s*$", text)
    if not m_head or not m_tail:
        return fail("sitemap.xml khong dung dinh dang urlset")
    blocks = re.findall(r"<url>.*?</url>", text, flags=re.S)
    if not blocks:
        return fail("sitemap.xml khong co muc <url> nao")
    kept, dropped = [], []
    for b in blocks:
        loc = re.search(r"<loc>(.*?)</loc>", b, flags=re.S)
        if not loc:
            return fail(f"muc <url> khong co <loc>: {b[:80]!r}")
        u = loc.group(1).strip()
        if u.startswith(base + "/"):
            kept.append(b)
        elif u.startswith(f"https://{other}/"):
            dropped.append(b)
        else:
            return fail(f"URL la khong thuoc domain nao: {u}")
    if not kept:
        return fail(f"khong giu duoc muc nao cho {dom}")
    # (Phuong an A) Build da loc theo ngon ngu nen sitemap thuong da theo
    # domain (khong co muc nao de bo) — do la truong hop binh thuong, KHONG
    # loi. Chi khi build gop (con muc cua domain kia) moi can loc.
    new_text = m_head.group(1) + "\n" + "\n".join(kept) + "\n</urlset>\n"
    sm.write_text(new_text, encoding="utf-8")

    # --- robots.txt: chi giu dong Sitemap cua domain nay ---
    lines = rb.read_text(encoding="utf-8").splitlines()
    kept_lines = []
    n_sitemap = 0
    for ln in lines:
        if ln.startswith("Sitemap:"):
            if ln.strip() == f"Sitemap: {base}/sitemap.xml":
                kept_lines.append(ln)
                n_sitemap += 1
            # dong Sitemap cua domain kia: bo
        else:
            kept_lines.append(ln)
    if n_sitemap != 1:
        return fail(f"robots.txt: con {n_sitemap} dong Sitemap (can dung 1, cua {dom})")
    rb.write_text("\n".join(kept_lines) + "\n", encoding="utf-8")

    # --- kiem lai thanh pham ---
    check = sm.read_text(encoding="utf-8")
    if f"https://{other}/" in check:
        return fail(f"sitemap.xml sau tach van con URL {other}")
    if f"https://{other}/" in rb.read_text(encoding="utf-8"):
        return fail(f"robots.txt sau tach van con {other}")
    if dropped:
        print(f"split-sitemap: CANH BAO — build gop (co {len(dropped)} loc {other}), "
              f"da loc thanh {dom} ({len(kept)}/{len(blocks)} loc); robots chi 1 dong Sitemap {dom}")
    else:
        print(f"split-sitemap: DAT ({dom}: sitemap da theo domain ({len(kept)} loc, "
              f"0 loc {other}); robots chi 1 dong Sitemap {dom})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
