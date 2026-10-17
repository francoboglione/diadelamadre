#!/usr/bin/env python3
"""Arma una carta lista para mandar: mete tus datos y tus fotos dentro de carta.html.

Uso:
  python3 armar.py datos.json --fotos mis-fotos/ -o para-mama.html
      Un solo archivo con las fotos adentro (achicadas a 1280 px). Se manda por
      WhatsApp o se sube a cualquier lado.

  python3 armar.py ejemplo/datos.json --sin-embeber -o index.html
      Deja las rutas de las fotos como están (para publicar la carpeta entera).

datos.json tiene los mismos campos que el bloque CARTA de carta.html. En "fotos"
podés poner rutas a archivos (relativas a datos.json); con --fotos se suman todas
las imágenes de esa carpeta, ordenadas por nombre.
Necesita Pillow (pip install pillow) solo para embeber fotos.
"""
import argparse
import base64
import io
import json
import os
import re
import sys

EXTENSIONES = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".heic", ".heif")
BLOQUE = re.compile(r"/\*CARTA:INICIO\*/.*?/\*CARTA:FIN\*/", re.S)


def foto_embebida(ruta, lado=1280, calidad=80):
    from PIL import Image, ImageOps
    try:
        import pillow_heif  # opcional, para fotos HEIC de iPhone
        pillow_heif.register_heif_opener()
    except ImportError:
        pass
    im = ImageOps.exif_transpose(Image.open(ruta)).convert("RGB")
    im.thumbnail((lado, lado))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=calidad, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def main():
    ap = argparse.ArgumentParser(description="Arma la carta para mamá.")
    ap.add_argument("datos", help="archivo JSON con los datos de la carta")
    ap.add_argument("--fotos", help="carpeta con fotos para sumar")
    ap.add_argument("--plantilla", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "carta.html"))
    ap.add_argument("--sin-embeber", action="store_true", help="no meter las fotos adentro del archivo")
    ap.add_argument("--lado", type=int, default=1280, help="lado máximo de cada foto en píxeles")
    ap.add_argument("-o", "--salida", default="para-mama.html")
    a = ap.parse_args()

    with open(a.datos, encoding="utf-8") as f:
        datos = json.load(f)
    base = os.path.dirname(os.path.abspath(a.datos))

    fotos = []
    for f in datos.get("fotos") or []:
        if isinstance(f, str):
            f = {"src": f}
        fotos.append(dict(f))
    if a.fotos:
        for nombre in sorted(os.listdir(a.fotos)):
            if nombre.lower().endswith(EXTENSIONES):
                fotos.append({"src": os.path.join(os.path.abspath(a.fotos), nombre), "texto": ""})

    salen = []
    for f in fotos:
        src = f.get("src", "")
        local = src if os.path.isabs(src) else os.path.join(base, src)
        if not a.sin_embeber and not re.match(r"^(data:|https?:)", src) and os.path.isfile(local):
            try:
                f["src"] = foto_embebida(local, a.lado)
            except Exception as e:  # una foto que no abre no frena la carta
                print("  (salteo %s: %s)" % (src, e), file=sys.stderr)
                continue
        salen.append(f)
    datos["fotos"] = salen

    with open(a.plantilla, encoding="utf-8") as f:
        html = f.read()
    if not BLOQUE.search(html):
        sys.exit("No encontré el bloque /*CARTA:INICIO*/ … /*CARTA:FIN*/ en la plantilla.")
    js = json.dumps(datos, ensure_ascii=False, indent=2).replace("</", "<\\/")
    html = BLOQUE.sub(lambda m: "/*CARTA:INICIO*/\nwindow.CARTA = " + js + ";\n/*CARTA:FIN*/", html, count=1)
    with open(a.salida, "w", encoding="utf-8") as f:
        f.write(html)
    print("Listo: %s (%d fotos, %.1f MB)" % (a.salida, len(salen), os.path.getsize(a.salida) / 1e6))


if __name__ == "__main__":
    main()
