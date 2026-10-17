#!/usr/bin/env python3
"""Arma una carta lista para mandar: mete tus datos y tus fotos dentro de carta.html.

Uso:
  python3 armar.py datos.json --fotos mis-fotos/ -o para-mama.html
      Un solo archivo con las fotos adentro (achicadas a 1280 px). Se manda por
      WhatsApp o se sube a cualquier lado. --fotos acepta una carpeta o un .zip.

  python3 armar.py ejemplo.json --sin-embeber -o index.html
      Deja las rutas de las fotos como están (para publicar la carpeta entera).

datos.json tiene los mismos campos que el bloque CARTA de carta.html (ver
INSTRUCCIONES-IA.md). En "fotos" podés poner rutas a archivos (relativas a
datos.json); con --fotos se suman todas las imágenes de esa carpeta o zip,
ordenadas por fecha de la foto (o por nombre si no tienen fecha).
Si "musica.archivo" es un mp3 local, también queda adentro del archivo.
Necesita Pillow (pip install pillow) solo para embeber fotos.
"""
import argparse
import base64
import io
import json
import os
import re
import sys
import tempfile
import zipfile

EXTENSIONES = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".heic", ".heif")
PALETAS = ("rosa", "lavanda", "durazno", "salvia", "cielo", "noche")
BLOQUE = re.compile(r"/\*CARTA:INICIO\*/.*?/\*CARTA:FIN\*/", re.S)


def abrir_imagen(ruta):
    from PIL import Image, ImageOps
    try:
        import pillow_heif  # opcional, para fotos HEIC de iPhone
        pillow_heif.register_heif_opener()
    except ImportError:
        pass
    return ImageOps.exif_transpose(Image.open(ruta))


def fecha_foto(ruta):
    """Fecha en que se sacó la foto (EXIF), o None."""
    try:
        from PIL import Image
        exif = Image.open(ruta).getexif()
        valor = exif.get(36867) or exif.get_ifd(0x8769).get(36867) or exif.get(306)
        return str(valor) if valor else None
    except Exception:
        return None


def foto_embebida(ruta, lado=1280, calidad=80):
    im = abrir_imagen(ruta).convert("RGB")
    im.thumbnail((lado, lado))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=calidad, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def imagenes_de(origen, temporal):
    """Lista de imágenes de una carpeta (recursiva) o de un .zip."""
    if zipfile.is_zipfile(origen):
        with zipfile.ZipFile(origen) as z:
            z.extractall(temporal)
        origen = temporal
    salida = []
    for base, carpetas, archivos in os.walk(origen):
        carpetas[:] = [c for c in carpetas if not c.startswith((".", "__MACOSX"))]
        for nombre in archivos:
            if nombre.lower().endswith(EXTENSIONES) and not nombre.startswith("."):
                salida.append(os.path.join(base, nombre))
    return salida


def main():
    ap = argparse.ArgumentParser(description="Arma la carta para mamá.")
    ap.add_argument("datos", help="archivo JSON con los datos de la carta")
    ap.add_argument("--fotos", help="carpeta o .zip con fotos para sumar")
    ap.add_argument("--orden", choices=("fecha", "nombre"), default="fecha",
                    help="cómo ordenar las fotos de --fotos (por defecto: fecha de la foto)")
    ap.add_argument("--plantilla", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "carta.html"))
    ap.add_argument("--sin-embeber", action="store_true", help="no meter fotos ni música adentro del archivo")
    ap.add_argument("--lado", type=int, default=1280, help="lado máximo de cada foto en píxeles")
    ap.add_argument("-o", "--salida", default="para-mama.html")
    a = ap.parse_args()

    with open(a.datos, encoding="utf-8") as f:
        datos = json.load(f)
    base = os.path.dirname(os.path.abspath(a.datos))
    avisos = []

    if isinstance(datos.get("paleta"), str) and datos["paleta"].lower() not in PALETAS:
        avisos.append("paleta '%s' no existe; se usa rosa" % datos["paleta"])

    fotos = []
    for f in datos.get("fotos") or []:
        fotos.append(dict(f) if isinstance(f, dict) else {"src": f})
    temporal = tempfile.mkdtemp(prefix="fotos-")
    if a.fotos:
        lista = imagenes_de(a.fotos, temporal)
        if a.orden == "fecha":
            fechas = {r: fecha_foto(r) for r in lista}
            lista.sort(key=lambda r: (fechas[r] is None, fechas[r] or "", os.path.basename(r).lower()))
        else:
            lista.sort(key=lambda r: os.path.basename(r).lower())
        fotos += [{"src": r, "texto": ""} for r in lista]

    salen = []
    for f in fotos:
        src = str(f.get("src", ""))
        local = src if os.path.isabs(src) else os.path.join(base, src)
        if not a.sin_embeber and not re.match(r"^(data:|https?:)", src) and os.path.isfile(local):
            try:
                f["src"] = foto_embebida(local, a.lado)
            except Exception as e:  # una foto que no abre no frena la carta
                avisos.append("salteé %s (%s)" % (os.path.basename(src), e.__class__.__name__))
                continue
        salen.append(f)
    datos["fotos"] = salen
    if len(salen) > 30:
        avisos.append("hay %d fotos: con más de 30 la carta se hace larga y el archivo pesado" % len(salen))

    musica = datos.get("musica") or {}
    arch = str(musica.get("archivo") or "")
    if arch and not a.sin_embeber and not re.match(r"^(data:|https?:)", arch):
        local = arch if os.path.isabs(arch) else os.path.join(base, arch)
        if os.path.isfile(local) and os.path.getsize(local) < 15e6:
            tipo = "audio/mp4" if local.lower().endswith((".m4a", ".mp4", ".aac")) else "audio/mpeg"
            with open(local, "rb") as fa:
                musica["archivo"] = "data:%s;base64,%s" % (tipo, base64.b64encode(fa.read()).decode("ascii"))
            datos["musica"] = musica
        else:
            avisos.append("no encontré la canción '%s' (o pesa más de 15 MB); queda la cajita de música" % arch)
            musica["archivo"] = ""
            datos["musica"] = musica

    with open(a.plantilla, encoding="utf-8") as f:
        html = f.read()
    if not BLOQUE.search(html):
        sys.exit("No encontré el bloque /*CARTA:INICIO*/ … /*CARTA:FIN*/ en la plantilla.")
    js = json.dumps(datos, ensure_ascii=False, indent=2).replace("</", "<\\/")
    html = BLOQUE.sub(lambda m: "/*CARTA:INICIO*/\nwindow.CARTA = " + js + ";\n/*CARTA:FIN*/", html, count=1)
    with open(a.salida, "w", encoding="utf-8") as f:
        f.write(html)
    print("Listo: %s (%d fotos, %.1f MB)" % (a.salida, len(salen), os.path.getsize(a.salida) / 1e6))
    for aviso in avisos:
        print("  Aviso: " + aviso)


if __name__ == "__main__":
    main()
