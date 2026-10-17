# Para agentes de IA

Si alguien te pide armar la carta para su mamá con este proyecto, seguí **[INSTRUCCIONES-IA.md](INSTRUCCIONES-IA.md)** de principio a fin: preguntás una sola vez, escribís los textos, armás `para-mama.html` con `armar.py` (fotos adentro) y lo entregás.

Si te piden cambiar el proyecto en sí:

- `carta.html` es la plantilla. Todo lo personalizable vive en el bloque entre `/*CARTA:INICIO*/` y `/*CARTA:FIN*/` (JSON válido); el resto es el motor, en JavaScript ES5 sin dependencias para que ande en celulares viejos.
- `index.html` se genera, no se edita a mano: `python3 armar.py ejemplo.json --sin-embeber -o index.html`.
- `clasico/` es la versión anterior; no la mezcles con la nueva.
- Probá en un ancho de celular (360 a 430 px): sin scroll horizontal, sin errores de consola, y con "Reducir movimiento" la carta tiene que aparecer completa.
