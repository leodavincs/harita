#!/usr/bin/env python3
"""Mind map data (JSON) -> one self-contained HTML page. Standard library only.

Usage:
  python3 kur.py data.json              -> data.html (same folder)
  python3 kur.py data.json -o map.html
  python3 kur.py data.json --ac         -> write and open in the browser
Format: ../references/bicim.md
"""
from __future__ import annotations

import argparse
import html
import json
import re
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


def main():
    ap = argparse.ArgumentParser(description="Harita verisini HTML'e çevirir")
    ap.add_argument("veri", type=Path)
    ap.add_argument("-o", "--cikti", type=Path)
    ap.add_argument("--ac", action="store_true", help="yazınca tarayıcıda aç")
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
    if a.ac:
        webbrowser.open(cikti.resolve().as_uri())


if __name__ == "__main__":
    main()
