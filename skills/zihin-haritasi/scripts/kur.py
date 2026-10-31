#!/usr/bin/env python3
"""Mind map data (JSON) -> one self-contained HTML page. Standard library only.

Usage:
  python3 kur.py data.json              -> data.html (same folder)
  python3 kur.py data.json -o map.html
  python3 kur.py data.json --ac         -> write and open in the browser
  python3 kur.py data.json --pdf        -> also write data.pdf (needs Chrome, Chromium or Edge)
Format: ../references/bicim.md
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import webbrowser
from pathlib import Path

SABLON = Path(__file__).resolve().parent.parent / "assets" / "sablon.html"
DUZENLER = {"harita", "mantik", "agac", "zaman", "kilcik", "matris"}


def oku(yol: Path) -> dict:
    metin = yol.read_text(encoding="utf-8")
    if yol.suffix == ".js":  # window.HARITA = {...};
        metin = re.sub(r"^\s*window\.HARITA\s*=\s*", "", metin.strip()).rstrip(";")
    return json.loads(metin)


def denetle(v: dict) -> list[str]:
    hatalar = []
    if "kok" not in v:
        if "dallar" not in v:
            return ["'kok' (ya da eski biçimde 'dallar') yok"]
        return []  # eski biçim, şablon çevirir
    if v.get("duzen", "harita") not in DUZENLER:
        hatalar.append(f"duzen bilinmiyor: {v.get('duzen')} (olanlar: {', '.join(sorted(DUZENLER))})")
    kimlik, cocuk = {}, {}

    def dolas(n, yol):
        if not n.get("ad"):
            hatalar.append(f"adı olmayan düğüm: {yol}")
        if "id" in n:
            if n["id"] in kimlik:
                hatalar.append(f"aynı id iki kez: {n['id']}")
            kimlik[n["id"]] = n
            cocuk[n["id"]] = len(n.get("alt", []))
        for i, c in enumerate(n.get("alt", [])):
            dolas(c, f"{yol} > {c.get('ad', i)}")

    dolas(v["kok"], v["kok"].get("ad", "kök"))
    for r in v.get("iliskiler", []):
        for uc in ("kaynak", "hedef"):
            if r.get(uc) not in kimlik:
                hatalar.append(f"ilişkide bilinmeyen {uc}: {r.get(uc)}")
    for tur in ("cerceveler", "ozetler"):
        for c in v.get(tur, []):
            if c.get("ust") not in kimlik:
                hatalar.append(f"{tur}: bilinmeyen ust {c.get('ust')}")
                continue
            a = c.get("aralik")
            if a and not (0 <= a[0] <= a[1] < cocuk[c["ust"]]):
                hatalar.append(f"{tur}: {c['ust']} için aralık {a} dal sayısı {cocuk[c['ust']]} ile uyuşmuyor")
    return hatalar


def kur(v: dict) -> str:
    sablon = SABLON.read_text(encoding="utf-8")
    veri = json.dumps(v, ensure_ascii=False).replace("</", "<\\/")
    baslik = v.get("baslik") or v.get("kok", {}).get("ad") or "Harita"
    return sablon.replace("__BASLIK__", html.escape(baslik)).replace("__VERI__", veri)


TARAYICILAR = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]


def tarayici_bul():
    adaylar = [os.environ.get("CHROME")] + TARAYICILAR
    adaylar += [shutil.which(a) for a in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome", "msedge")]
    return next((a for a in adaylar if a and Path(a).exists()), None)


def pdf_yaz(sayfa: Path, pdf: Path) -> bool:
    """Sayfayı başsız tarayıcıyla açar; ?yazdir=1 haritayı A4 yataya sığdırır, ayrıntıları sonraki sayfalara açar."""
    tarayici = tarayici_bul()
    if not tarayici:
        print("PDF için Chrome, Chromium ya da Edge bulunamadı. Sayfayı açıp sağ üstteki PDF düğmesine bas.", file=sys.stderr)
        return False
    subprocess.run([tarayici, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=5000", "--window-size=1123,794",
                    f"--print-to-pdf={pdf}", sayfa.resolve().as_uri() + "?yazdir=1"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    return pdf.exists()


def main():
    ap = argparse.ArgumentParser(description="Harita verisini HTML'e çevirir")
    ap.add_argument("veri", type=Path)
    ap.add_argument("-o", "--cikti", type=Path)
    ap.add_argument("--ac", action="store_true", help="yazınca tarayıcıda aç")
    ap.add_argument("--pdf", action="store_true", help="aynı adla PDF de yaz")
    a = ap.parse_args()
    v = oku(a.veri)
    hatalar = denetle(v)
    if hatalar:
        print("Veri hatalı:\n- " + "\n- ".join(hatalar), file=sys.stderr)
        sys.exit(1)
    cikti = a.cikti or a.veri.with_suffix(".html")
    if cikti.resolve() == a.veri.resolve():
        cikti = a.veri.with_name(a.veri.stem + "-harita.html")
    cikti.parent.mkdir(parents=True, exist_ok=True)
    cikti.write_text(kur(v), encoding="utf-8")
    print(cikti)
    if a.pdf and pdf_yaz(cikti, cikti.with_suffix(".pdf")):
        print(cikti.with_suffix(".pdf"))
    if a.ac:
        webbrowser.open(cikti.resolve().as_uri())


if __name__ == "__main__":
    main()
