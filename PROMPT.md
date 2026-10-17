# Hacé la carta para tu mamá con ChatGPT o Claude

Sin instalar nada y sin saber de computación. En 5 minutos tenés una carta animada: un sobre que se abre, la carta que se escribe sola, tus fotos que caen y pasan en carrusel, y al final todas forman un corazón.

👉 **Mirá cómo queda:** [carta de ejemplo](https://francoboglione.github.io/diadelamadre/)

---

## La forma más fácil: subí el proyecto entero

1. **Descargá el proyecto:** tocá **[este link](https://github.com/francoboglione/diadelamadre/archive/refs/heads/main.zip)** (funciona igual en el celu y en la compu). Se baja un archivo `diadelamadre-main.zip`. No hace falta abrirlo.
2. **Abrí un chat nuevo** en [chatgpt.com](https://chatgpt.com) o en [claude.ai](https://claude.ai).
3. **Adjuntá** el zip y entre 10 y 20 fotos (del celu, o desde Google Drive con el clip 📎). Si querés, también una canción en mp3.
4. **Escribí esto y mandalo:**

   ```text
   Armame la carta para mi mamá con este proyecto. Seguí las instrucciones de INSTRUCCIONES-IA.md que está adentro del zip.
   ```

5. **Contestá las preguntas** (cómo le dicen, quiénes firman, cómo es ella, algo para destacar, colores y canción). Si no tenés ganas, escribí "dale con lo que quieras".
6. **Descargá `para-mama.html`**, abrilo y tocá el sobre.

Para esto, ChatGPT o Claude tienen que poder **leer archivos y correr código**: así meten las fotos adentro de la carta. ChatGPT lo hace solo. En Claude, si te dice que no puede ejecutar código, activá la creación de archivos en *Configuración*.

¿No podés subir el zip? Bajá solo [`carta.html`](https://raw.githubusercontent.com/francoboglione/diadelamadre/main/carta.html) (en el celu: mantené apretado el link → *Descargar vínculo*), adjuntalo con tus fotos y usá [el prompt largo](#el-prompt-largo) de más abajo.

## Cómo mandarla

- **Por WhatsApp, como archivo.** En Android se abre directo. En iPhone a veces no anima: mejor mandá un link.
- **Con un link gratis.** Renombrá el archivo a `index.html`, ponelo solo en una carpeta y arrastrá la carpeta a [app.netlify.com/drop](https://app.netlify.com/drop). Te da un link al instante; creá una cuenta gratis para que no se borre.
- **Si te la mostró como artifact de Claude o en el Canvas de ChatGPT**, usá el botón Compartir.
- Truco: si al link le agregás `#Marta` al final, la carta dice "Querida Marta".

---

## El prompt largo

Solo si adjuntaste `carta.html` suelto (sin el zip). Copiá todo lo que está en el recuadro:

````text
Quiero regalarle a mi mamá una carta animada por el Día de la Madre. Te adjunto carta.html (plantilla de código abierto del proyecto github.com/francoboglione/diadelamadre, licencia MIT) y mis fotos.

PASO 1 · PREGUNTAS
Haceme estas preguntas todas juntas, en un solo mensaje corto y cálido, y aclarame que si no contesto algo usás lo de por defecto. Si alguna ya la contesté en este mensaje, no la repitas.
1. ¿Cómo le dicen? (mamá, ma, mami, su nombre) · por defecto "mamá"
2. ¿Quiénes firman? (nombres) · por defecto "Tus hijos"
3. Contame cómo es ella: algo que siempre dice, algo que cocina o hace, una costumbre suya
4. Algo para destacar: un momento, un logro o algo que hizo por ustedes
5. Colores: rosa, lavanda, durazno, salvia, cielo o noche · por defecto rosa
6. ¿Querés una canción propia? Subí el mp3 y decime en qué segundo arranca · si no, suena una cajita de música
No me pidas nada más.

PASO 2 · TEXTOS
Con mis respuestas, escribí los textos de la carta:
- Cálidos, simples y concretos, como habla una familia. Escribí como escribo yo (si uso "vos", con voseo).
- "hijos" es la cantidad de personas que firman: 1 = todo en singular ("te escribí"), 2 o más = plural ("te escribimos").
- Usá los detalles que te di (frases, comidas, costumbres) en "recuerdos", "gracias" y "pd". Si tenés algo concreto, nada genérico.
- "destacado": una o dos oraciones, la parte más emotiva, basada en lo que me pediste destacar.
- "gracias": 4 o 5 frases cortas que empiecen con "Por…"; la última, corta y fuerte (por ejemplo "Por estar. Siempre.").
- Si no me contestás nada, dejá "textos" vacío: la plantilla trae textos lindos por defecto.
- Mirá las fotos y ordenalas de la más vieja a la más nueva. Poné pie de foto solo si estás seguro de lo que muestra (2 a 4 palabras).

PASO 3 · ARMAR EL ARCHIVO
En carta.html reemplazá SOLO lo que está entre /*CARTA:INICIO*/ y /*CARTA:FIN*/ por:
window.CARTA = { ...tus datos en JSON... };
No cambies nada más del archivo. Formato (lo que no sepas, dejalo como está):
{
  "para": "mamá",
  "de": "Lucía, Tomi y Juli",
  "hijos": 3,
  "fecha": "Domingo 18 de octubre",
  "paleta": "rosa",
  "textos": {
    "saludo": "Querida {para}:",
    "intro": "...", "recuerdos": "...",
    "antesDestacado": "Hay algo que queremos que sepas:", "destacado": "...",
    "gracias": ["Por ...", "Por ...", "Por ...", "Por estar. Siempre."],
    "final": "...",
    "cierre": "Feliz día, {para}", "sub": "A la mejor mamá del mundo.",
    "firma": "Con amor,", "pd": "P. D.: ..."
  },
  "fotos": [ { "src": "...", "texto": "" } ],
  "musica": { "archivo": "", "desde": 0, "generada": true },
  "mostrarComoHacerla": false
}
{para} se reemplaza solo por el nombre. "fecha" es el Día de la Madre de mi país (en Argentina 2026: "Domingo 18 de octubre").

OPCIÓN A, la mejor (si podés ejecutar Python): meté las fotos adentro del archivo, achicadas, con este código, y dame para-mama.html para descargar.

import base64, io, json, re
from PIL import Image, ImageOps
def foto(ruta):
    im = ImageOps.exif_transpose(Image.open(ruta)).convert("RGB")
    im.thumbnail((1280, 1280))
    b = io.BytesIO(); im.save(b, "JPEG", quality=80, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
datos = { ... }  # todo menos las fotos
datos["fotos"] = [{"src": foto(ruta), "texto": pie} for ruta, pie in FOTOS_EN_ORDEN]
html = open("carta.html", encoding="utf-8").read()
js = json.dumps(datos, ensure_ascii=False).replace("</", "<\\/")
html = re.sub(r"/\*CARTA:INICIO\*/.*?/\*CARTA:FIN\*/",
              lambda m: "/*CARTA:INICIO*/\nwindow.CARTA = " + js + ";\n/*CARTA:FIN*/", html, flags=re.S)
open("para-mama.html", "w", encoding="utf-8").write(html)

Si una foto no abre (por ejemplo HEIC de iPhone), salteala y avisame cuál. Si te pasé un mp3, metelo igual como "data:audio/mpeg;base64,..." en musica.archivo.

OPCIÓN B (si no podés ejecutar Python, en Canvas o como artifact): mostrame el archivo carta.html COMPLETO con mi bloque CARTA, sin resumir ni cortar nada. En "fotos" usá los links públicos de Google Drive que te pase (la plantilla los convierte sola). Avisame que las fotos subidas al chat no se pueden meter sin Python, y que si las fotos no aparecen, lo mejor es la opción A.

PASO 4 · AL FINAL
Decime en 3 líneas cómo probarla (abrir el archivo y tocar el sobre) y cómo mandarla.
````

---

## Así se ve la charla

> **Vos:** *(adjuntás el zip y 14 fotos)* Armame la carta para mi mamá con este proyecto. Seguí las instrucciones de INSTRUCCIONES-IA.md que está adentro del zip.
>
> **IA:** ¡Qué lindo regalo! Te hago 6 preguntas rápidas; lo que no contestes lo completo yo: 1) ¿Cómo le dicen? 2) ¿Quiénes firman? 3) ¿Qué dice siempre, qué cocina, qué costumbre tiene? 4) ¿Algo para destacar? 5) ¿Colores: rosa, lavanda, durazno, salvia, cielo o noche? 6) ¿Canción propia?
>
> **Vos:** Le decimos ma. Firmamos Lucía, Tomi y Juli. Siempre dice "¿comiste?", hace las mejores milanesas y manda audios de 4 minutos. Destacá que volvió a estudiar a los 45 y se recibió. Lavanda. Sin canción.
>
> **IA:** ¡Listo! Te armé la carta con tus 14 fotos adentro: **para-mama.html**. Abrila, tocá el sobre y subí el volumen. Para mandarla…

Quedaría así: [ver el ejemplo](https://francoboglione.github.io/diadelamadre/).

## Preguntas frecuentes

**¿Puedo cambiar algo después?** Sí, en el mismo chat: "cambiá la P. D. por…", "pasala a colores durazno", "sacá la foto 3". Te devuelve el archivo nuevo.

**¿Por qué tengo que tocar el sobre para que suene?** Los celulares no dejan que una página haga ruido sola. El toque en el sobre es el que destraba la música.

**¿Las fotos quedan en algún lado?** Quedan adentro de tu archivo, nada más. Si lo subís a un link, cualquiera que tenga el link puede verla (no aparece en buscadores).

**¿Y si no tengo fotos a mano?** La carta funciona igual, con flores dibujadas en lugar de fotos.
