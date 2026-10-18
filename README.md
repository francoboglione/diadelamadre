# Carta para mamá 💌

Una carta animada para el Día de la Madre que **armás desde ChatGPT o Claude, sin saber de computación**. Se abre un sobre, la carta se escribe sola mientras la página baja, tus fotos caen como lluvia y pasan en carrusel, una frase se resalta como con marcador y al final todas las fotos forman un corazón. Con música.

👉 **Ejemplo:** [francoboglione.github.io/diadelamadre](https://francoboglione.github.io/diadelamadre/) (la carta de "Marta", con fotos de ejemplo)

- **Gratis y de código abierto** (licencia MIT).
- **Un solo archivo**, con las fotos adentro: se manda por WhatsApp o se sube a un link.
- **Pensada para el celular** (iPhone y Android, también teléfonos viejos). En compu se ve como una hoja sobre el escritorio.
- **Seis paletas de colores** y textos que se adaptan si firma uno o varios hijos.

---

## Hacela en 5 minutos

1. **Descargá el proyecto:** [diadelamadre-main.zip](https://github.com/francoboglione/diadelamadre/archive/refs/heads/main.zip) (anda en el celu y en la compu; no hace falta abrirlo).
2. **Abrí un chat en [ChatGPT](https://chatgpt.com) o [Claude](https://claude.ai)** y adjuntá el zip y entre 10 y 20 fotos (del celu o desde Google Drive).
3. **Mandá esta frase:**

   ```text
   Armame la carta para mi mamá con este proyecto. Seguí las instrucciones de INSTRUCCIONES-IA.md que está adentro del zip.
   ```

La IA te hace 6 preguntas (cómo le dicen, quiénes firman, cómo es ella, algo para destacar, colores y canción), escribe los textos, ordena las fotos por fecha y te devuelve **`para-mama.html`** con todo adentro. Si no contestás alguna pregunta, usa lo de por defecto: la carta siempre sale completa.

Paso a paso con un ejemplo de la charla, cómo mandarla y la alternativa sin zip: [`PROMPT.md`](PROMPT.md).

## Qué le podés pedir

| | Opciones |
|---|---|
| **Cómo le dicen** | mamá, ma, mami, su nombre |
| **Quiénes firman** | uno o varios: los textos pasan solos a singular o plural |
| **Colores** | `rosa` · `lavanda` · `durazno` · `salvia` · `cielo` · `noche` |
| **Algo para destacar** | aparece resaltado con marcador en el medio de la carta |
| **Música** | tu mp3 (y desde qué segundo) o una cajita de música incluida, sin derechos |
| **Fotos** | subidas al chat (quedan adentro del archivo) o links públicos de Google Drive |

Después podés pedir cambios en el mismo chat: "cambiá la P. D.", "pasala a durazno", "sacá la foto 3".

## Cómo mandarla

- **WhatsApp:** mandá `para-mama.html` como archivo. En Android se abre directo; en iPhone conviene un link.
- **Link gratis:** renombrala `index.html`, ponela sola en una carpeta y arrastrá la carpeta a [app.netlify.com/drop](https://app.netlify.com/drop).
- **Artifact de Claude o Canvas de ChatGPT:** botón Compartir.
- **Truco:** agregá `#Nombre` al final del link y la carta dice "Querida Nombre".

---

## Para los que se animan a un poco más

Todo lo que se personaliza está en un solo bloque al principio de `carta.html`, entre `/*CARTA:INICIO*/` y `/*CARTA:FIN*/`:

```js
window.CARTA = {
  "para": "mamá",
  "de": "Lucía, Tomi y Juli",
  "hijos": 3,
  "fecha": "Domingo 18 de octubre",
  "paleta": "rosa",
  "textos": { "destacado": "Cuando volviste a estudiar a los 45…" },
  "fotos": [{ "src": "fotos/01.jpg", "texto": "La costa, 1998" }],
  "musica": { "archivo": "", "generada": true }
};
```

### Extras opcionales

- **Poema** (`textos.poema`): una lista de estrofas, con los versos separados por `\n`. Se reparten a lo largo de la carta y la última queda antes del cierre.
- **Regalos** (`regalos`): tarjetas al final de la carta. Las entregadas llevan un tilde; las que tienen `pista`, `perras` o `hasta` se dan vuelta al tocarlas.

```js
"regalos": { "titulo": "Y como hoy es tu día, los regalos:", "lista": [
  { "icono": "💐", "titulo": "Flores", "texto": "…", "entregado": true },
  { "icono": "🎁", "titulo": "Regalo misterioso", "pista": "Te va a acompañar cada mañana…",
    "perras": [{ "nombre": "Suki", "raza": "pug" }, { "nombre": "Nina", "raza": "bulldog" }] },
  { "icono": "✈️", "titulo": "Un regalo te espera en Barcelona", "pista": "…", "hasta": "2026-10-27" }
] }
```

- **Línea de tiempo** (`hitos`): cifras grandes arriba y fechas que aparecen una por una. `{ "titulo": "…", "cifras": [{ "n": 4, "t": "hijos" }], "lista": [{ "fecha": "14 de septiembre de 1962", "titulo": "Nace Rossana", "texto": "…", "logro": true }] }`
- **Locuras** (`locuras`): las mismas tarjetas que los regalos, para anécdotas. Las tarjetas aceptan `foto` (adelante), `fotoAtras` (al darla vuelta) y `chip` (una etiqueta).
- **Letra grande** (`"lectura": "grande"`): texto y botones más grandes, pensado para abuelas. Con `"velocidad": 0.85` se escribe más despacio.
- **Celulares con poca memoria**: la carta lo detecta sola y usa menos pétalos y sombras más simples.
- **Canción por link** (`musica.enlace`): `{ "texto": "🎶 Primero, poné Mamma Mia", "url": "https://open.spotify.com/…", "nota": "…" }`. Muestra un botón en el sobre que abre la canción en Spotify o YouTube; si lo toca, la cajita de música no suena encima.

Los textos que no pongas (`saludo`, `intro`, `recuerdos`, `antesDestacado`, `destacado`, `gracias`, `final`, `cierre`, `sub`, `firma`, `pd`) se completan solos. También acepta `"velocidad": 1.5` para que se escriba más rápido, y una paleta propia con colores (`{"fondo": "#…", "papel": "#…", "acento": "#…"}`).

**Con Python**, `armar.py` hace lo mismo que la IA: achica las fotos y las mete adentro.

```bash
pip install pillow
python3 armar.py mis-datos.json --fotos carpeta-de-fotos/ -o para-mama.html
```

El ejemplo de este repo se genera con `python3 armar.py ejemplo.json --sin-embeber -o index.html`.

**Con GitHub Pages:** hacé un fork, cambiá el bloque de `carta.html`, subí tus fotos a `fotos/` y activá *Settings → Pages → main / root*.

## Sonidos

Además de la música, la carta tiene efectos sintetizados y bajitos (sin archivos): el lacre al abrir, un tecleo suave mientras escribe, un soplido cuando cae cada foto, el marcador, las notitas de la lista, las tarjetas que se dan vuelta y unas campanitas al final. El botón **Sonido** apaga todo junto. En iPhone suena aunque el celular esté en silencio, y si iOS corta el audio al volver de otra app, se reanuda con el siguiente toque. Con `"sonidos": false` se desactivan, y con "Reducir movimiento" no suenan.

## Pruebas

`python3 pruebas/qa.py carta-armada.html` (necesita Playwright) recorre la carta en 360, 390, 430 y 1280 px: sin scroll horizontal ni errores, recorrido completo con la pluma siempre a la vista, tocar la pantalla frena el seguimiento y lo retoma, Pausar y Sonido, tarjetas de regalos, cuenta regresiva y "Reducir movimiento".

## Cómo funciona

1. Un sobre con lacre de corazón y "Para mamá" escrito a mano. Al tocarlo arranca la música, se abre la solapa y sale la carta.
2. La carta ocupa la pantalla y se escribe letra por letra. La página baja sola siguiendo lo que se escribe; abajo hay **Pausar**, **Ver todo** y **Sonido**.
3. En el medio, la **lluvia de fotos**, el **carrusel**, la frase **resaltada**, la lista de **gracias** y el **corazón de fotos**.
4. Cierra con "Feliz día, mamá", la firma y la P. D.

Sin dependencias, JavaScript ES5 para celulares viejos, y respeta "Reducir movimiento" (muestra la carta completa, sin animaciones).

## Estructura

```
carta.html            la plantilla: motor + bloque de datos
INSTRUCCIONES-IA.md   lo que lee ChatGPT o Claude para armar la carta (preguntas, textos, armado)
PROMPT.md             paso a paso para la persona, y un prompt largo si solo sube carta.html
armar.py              arma la carta con Python: fotos (carpeta o zip) ordenadas por fecha y adentro del archivo
AGENTS.md, CLAUDE.md  apuntan a INSTRUCCIONES-IA.md para que cualquier IA lo encuentre
index.html     la carta de ejemplo (generada desde ejemplo.json)
ejemplo.json   los datos del ejemplo
fotos/         fotos de ejemplo (ilustraciones generadas)
clasico/       la versión anterior: historia en 5 capítulos con 4 formatos
```

## Versión clásica

La versión anterior (historias tipo Instagram, cine, carta con scroll y álbum de polaroids) sigue en [`clasico/`](clasico/), con su propio `historia.js` y la guía [`clasico/PROMPT-CLAUDE.md`](clasico/PROMPT-CLAUDE.md).

## Privacidad

La página no se indexa en buscadores, pero **cualquiera que tenga el link la puede ver**. Usá fotos que la familia esté de acuerdo en compartir.

## Licencia

[MIT](LICENSE). Usala, cambiala y regalala. Si la mejorás, mandá un *pull request*.
