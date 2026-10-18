# Instrucciones para la IA (ChatGPT, Claude u otra)

Estás ayudando a alguien a armar una **carta animada para su mamá** con este proyecto (código abierto, licencia MIT). La persona no sabe programar: hablale simple, cálido y corto, sin jerga técnica. Tu trabajo termina cuando le entregás **un archivo `para-mama.html` listo para abrir y mandar**.

Qué hace la carta: se abre un sobre, la carta se escribe sola mientras la página baja, caen las fotos (lluvia), pasan en carrusel, una frase se resalta con marcador, hay una lista de "Gracias por…", todas las fotos forman un corazón y cierra con "Feliz día, mamá", la firma y una P. D. Tiene música (una cajita generada o el mp3 que te pasen).

Archivos que importan:

| Archivo | Para qué |
|---|---|
| `carta.html` | La plantilla: motor + un bloque de datos entre `/*CARTA:INICIO*/` y `/*CARTA:FIN*/`. Es lo único que se modifica. |
| `armar.py` | Arma `para-mama.html`: mete los datos, achica las fotos (1280 px), las ordena por fecha y las deja adentro del archivo. |
| `ejemplo.json` | Un ejemplo completo de datos (mamá ficticia, tres hijos). |

No toques nada de `clasico/` (es una versión vieja).

---

## Paso 1 · Preguntas (una sola vez)

Si la persona todavía no subió fotos, pedíselas primero (entre 10 y 20; del celu o desde Google Drive con el botón de adjuntar; un .zip también sirve).

Después hacé **todas estas preguntas juntas, en un solo mensaje**, aclarando que si no contesta algo usás lo de por defecto. No preguntes lo que ya te dijo.

1. ¿Cómo le dicen? (mamá, ma, mami, su nombre) · por defecto "mamá"
2. ¿Quiénes firman? (nombres) · por defecto "Tus hijos"
3. Contame cómo es ella: algo que siempre dice, algo que cocina o hace, una costumbre suya
4. Algo para destacar: un momento, un logro o algo que hizo por ustedes
5. Colores: rosa, lavanda, durazno, salvia, cielo o noche · por defecto rosa
6. ¿Querés una canción propia? Subí el mp3 y decime en qué segundo arranca · si no, suena una cajita de música

Si responde "dale", "lo que quieras" o no responde algo, seguí con lo de por defecto. No hagas una segunda ronda de preguntas salvo que falte algo imprescindible (por ejemplo, no hay ninguna foto y la persona quería fotos).

## Paso 2 · Textos

Escribí los textos de la carta:

- **Voz:** cálida, simple y concreta, como habla una familia. Escribí como escribe la persona: si usa "vos", con voseo; si usa "tú", con tuteo.
- **Número:** `hijos` = cantidad de personas que firman. 1 = singular ("te escribí", "me cuidaste"); 2 o más = plural ("te escribimos").
- **Detalles reales:** usá lo que te contó (frases suyas, comidas, costumbres) en `recuerdos`, `gracias` y `pd`. Si tenés algo concreto, nada genérico.
- **`destacado`:** una o dos oraciones, la parte más emotiva, basada en lo que pidió destacar.
- **`gracias`:** 4 o 5 frases cortas que empiecen con "Por…"; la última, corta y fuerte ("Por estar. Siempre.").
- **`pd`:** algo con humor o ternura, de la familia.
- **Largo:** cada párrafo de 1 a 3 oraciones. La carta tiene que leerse en 2 o 3 minutos.
- Si la persona no te dio nada para personalizar, dejá `textos` vacío (`{}`): la plantilla trae textos lindos por defecto, en singular o plural según `hijos`.
- `{para}` dentro de un texto se reemplaza solo por cómo le dicen.

## Paso 3 · Datos

Armá un `datos.json` así (lo que no sepas, dejalo como está):

```json
{
  "para": "mamá",
  "de": "Lucía, Tomi y Juli",
  "hijos": 3,
  "fecha": "Domingo 18 de octubre",
  "paleta": "rosa",
  "textos": {
    "saludo": "Querida {para}:",
    "intro": "...",
    "recuerdos": "...",
    "antesDestacado": "Hay algo que queremos que sepas:",
    "destacado": "...",
    "gracias": ["Por ...", "Por ...", "Por ...", "Por estar. Siempre."],
    "final": "...",
    "cierre": "Feliz día, {para}",
    "sub": "A la mejor mamá del mundo.",
    "firma": "Con amor,",
    "pd": "P. D.: ..."
  },
  "fotos": [],
  "musica": { "archivo": "", "desde": 0, "generada": true },
  "mostrarComoHacerla": false
}
```

- `fecha`: el Día de la Madre de su país. En Argentina 2026 es "Domingo 18 de octubre"; si no sabés el país, "Día de la Madre".
- `fotos`: dejalo vacío si vas a usar `--fotos` (abajo). Si querés un orden o pies de foto propios, listalas vos: `{"src": "ruta/a/la/foto.jpg", "texto": "La costa, 1998"}`. Poné pie de foto solo si estás seguro de lo que muestra (2 a 4 palabras).
- `musica.archivo`: la ruta al mp3 si te pasaron uno (queda adentro del archivo); `desde` = segundo en que arranca.
- Colores propios: en vez de un nombre, `"paleta": {"fondo": "#3a1f2b", "papel": "#fff8f2", "acento": "#c9506e"}`.
- Extras opcionales (`textos.poema`, `regalos`, `musica.enlace`): ver la sección "Extras opcionales" del README. Usalos solo si la persona pide un poema, quiere contar regalos o pide una canción que no tiene en mp3.
- `velocidad` (opcional): 1 = normal, 1.5 = más rápida.

## Paso 4 · Armar el archivo

### Si podés ejecutar Python (lo mejor)

1. Si te subieron el proyecto en .zip, descomprimilo. Si las fotos vinieron en .zip, no hace falta descomprimirlas.
2. Corré, desde la carpeta del proyecto:

   ```bash
   python3 armar.py datos.json --fotos CARPETA_O_ZIP_DE_FOTOS -o para-mama.html
   ```

   `--fotos` toma todas las imágenes de esa carpeta (o zip), las ordena por la fecha en que se sacaron, las achica y las mete adentro. Las fotos que no abren (por ejemplo HEIC sin soporte) se saltean con un aviso: decile a la persona cuáles y que las mande como JPG o captura.
3. Guardá `para-mama.html` donde tu entorno deje descargar archivos (en ChatGPT, `/mnt/data/`; en Claude, `/mnt/user-data/outputs/`) y dale el link de descarga.

Si no tenés `armar.py` (solo te pasaron `carta.html`), hacé lo mismo con este código:

```python
import base64, io, json, re
from PIL import Image, ImageOps
def foto(ruta):
    im = ImageOps.exif_transpose(Image.open(ruta)).convert("RGB")
    im.thumbnail((1280, 1280))
    b = io.BytesIO(); im.save(b, "JPEG", quality=80, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
datos = json.load(open("datos.json", encoding="utf-8"))
datos["fotos"] = [{"src": foto(r), "texto": ""} for r in FOTOS_EN_ORDEN]
html = open("carta.html", encoding="utf-8").read()
js = json.dumps(datos, ensure_ascii=False).replace("</", "<\\/")
html = re.sub(r"/\*CARTA:INICIO\*/.*?/\*CARTA:FIN\*/",
              lambda m: "/*CARTA:INICIO*/\nwindow.CARTA = " + js + ";\n/*CARTA:FIN*/", html, flags=re.S)
open("para-mama.html", "w", encoding="utf-8").write(html)
```

### Si no podés ejecutar Python (Canvas de ChatGPT o artifact de Claude)

Mostrá `carta.html` **completo**, sin resumir ni cortar nada, cambiando solo el bloque entre `/*CARTA:INICIO*/` y `/*CARTA:FIN*/` por `window.CARTA = { ...datos... };`. Las fotos subidas al chat no se pueden meter sin Python: usá links públicos de Google Drive si te los pasa (la plantilla los convierte sola) o dejá `fotos` vacío. Avisale que la carta tiene el botón "Probar con mis fotos" para verla con sus fotos en su celu, y que para mandarla con fotos lo mejor es hacerlo con un chat que pueda ejecutar código.

## Paso 5 · Antes de entregar, revisá

- `datos.json` es JSON válido (comillas dobles, sin comas sobrantes).
- El archivo final tiene el bloque reemplazado una sola vez y el resto de `carta.html` intacto.
- La cantidad de fotos que entraron coincide con las que subió (avisá las que se saltearon).
- El archivo pesa menos de 15 MB (con 20 fotos suele andar en 3 o 4 MB).

## Paso 6 · Entrega

Entregá el archivo y, en pocas líneas:

1. **Probala:** abrí el archivo y tocá el sobre (con volumen).
2. **Mandala:** por WhatsApp como archivo (en Android se abre directo), o para tener un link: renombrarla `index.html`, ponerla sola en una carpeta y arrastrar la carpeta a app.netlify.com/drop.
3. **Truco:** agregando `#Nombre` al final del link, la carta dice "Querida Nombre".

Ofrecé cambios: "¿Querés que cambie algún texto, los colores o el orden de las fotos?". Para cada cambio, volvé a armar el archivo completo.
