# Armala desde Claude (sin GitHub)

En 5 minutos y sin instalar nada. Vas a terminar con un link público para mandar por WhatsApp.

## Qué necesitás

1. **`index.html` y `historia.js`** de este repositorio (*Code → Download ZIP*, o abrí cada archivo y tocá *Download raw file*).
2. **Tus fotos**: entre 12 y 20, en JPG. Si pesan mucho, achicalas antes en [squoosh.app](https://squoosh.app).
3. **La canción** (opcional), en mp3.

## Paso a paso

1. Abrí un chat nuevo en [claude.ai](https://claude.ai).
2. Adjuntá `index.html`, `historia.js`, las fotos y la canción.
3. Copiá el prompt de abajo, completá lo que está entre corchetes y mandalo.
4. Cuando Claude publique el artifact, abrilo, tocá **Compartir** y copiá el link.

---

## El prompt

```
Quiero regalarle a mi mamá una página por el Día de la Madre. Te adjunto index.html
e historia.js del proyecto "diadelamadre" (código abierto, licencia MIT), mis fotos
y una canción.

Hacé esto:

1. Editá historia.js con mi historia. NO toques index.html (es el motor y ya funciona):
   - Formato (tema): [historias | cine | carta | album]
   - Cómo le decimos: [Mamá / Ma / Mami / su nombre]
   - Quiénes firman: [ej: "Lucía, Tomi y Juli"]
   - Capítulos (4 o 5). Para cada uno: título, una frase corta, qué fotos van
     (en orden) y una frase "golpe" que cierra el capítulo.
       1. [título] — [frase] — fotos: [nombres de archivo] — golpe: [frase]
       2. ...
     Si no te paso textos, escribilos vos en español rioplatense, con voseo,
     cálidos y simples, de menor a mayor emoción (el capítulo 4 es el más fuerte).
   - Mensaje final: [o escribilo vos]
   - Canción: que arranque en el segundo [X] (justo antes del estribillo).

2. Poné las fotos en una carpeta fotos/ y respetá los nombres en historia.js.

3. Publicá index.html como artifact, con historia.js, las fotos y musica.mp3
   como archivos del mismo artifact (en las mismas rutas). Si no podés subir
   archivos aparte, comprimí las fotos a 1200 px e incrustalas en historia.js.

4. Revisá que funcione en celular (iPhone y Android) y pasame el link.
```

---

## Preguntas frecuentes

**¿El link es público?**
El artifact empieza privado. Cuando tocás **Compartir** (o *Publicar*), cualquiera con el link lo puede ver. No aparece en buscadores.

**¿Puedo cambiar algo después?**
Sí. En el mismo chat pedile: "cambiá la frase del capítulo 3 por…" o "pasalo a formato cine". El link sigue siendo el mismo.

**¿Por qué tengo que tocar la pantalla para que suene la música?**
Los celulares no dejan que una página reproduzca sonido sola. El primer toque ("tocá para abrir") es el que la destraba.
