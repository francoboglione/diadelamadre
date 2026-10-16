/*
 * ─────────────────────────────────────────────────────────────
 *  TU HISTORIA  ·  Este es el único archivo que tenés que editar
 * ─────────────────────────────────────────────────────────────
 *
 *  1. Poné tus fotos en la carpeta /fotos (JPG, idealmente de menos de 400 KB).
 *  2. Si querés música, subí un archivo llamado musica.mp3 al lado de este archivo.
 *  3. Cambiá los textos de abajo. Respetá las comillas y las comas.
 *
 *  Truco: podés probar cualquier formato agregando ?tema=cine (o carta,
 *  historias, album) al final del link, sin tocar nada.
 */
window.HISTORIA = {

  // Formato de la página: "historias" | "cine" | "carta" | "album"
  tema: "historias",

  // Cómo le dicen a ella y quiénes firman
  para: "Mamá",
  de: "Tus hijos",
  fecha: "Domingo 18 de octubre",

  // Pantalla de inicio
  portada: {
    titulo: "Una historia para vos",
    bajada: "Cinco capítulos. Subí el volumen y tocá para empezar."
  },

  // Canción de fondo (opcional). Elegila vos: la que les recuerde a ella.
  // "desde" = en qué segundo arranca (ideal: justo antes del estribillo).
  musica: {
    archivo: "musica.mp3",
    titulo: "La canción que elegimos para vos",
    desde: 0,
    volumen: 0.85
  },

  // Segundos que dura cada foto en los formatos automáticos (historias y cine)
  ritmo: 4.5,

  // La historia: 4 o 5 capítulos funcionan mejor.
  // Cada foto puede ser "fotos/01.jpg" o { src: "fotos/01.jpg", texto: "Pie de foto" }.
  // También acepta videos cortos: { src: "videos/a.mp4", poster: "videos/a.jpg" }
  capitulos: [
    {
      titulo: "Donde empezó todo",
      frase: "Antes de conocer el mundo, te conocimos a vos.",
      fotos: [
        { src: "fotos/01.jpg", texto: "Los primeros días" },
        { src: "fotos/02.jpg", texto: "Siempre a upa" },
        { src: "fotos/03.jpg" }
      ],
      golpe: "Lo primero que aprendimos a decir fue tu nombre."
    },
    {
      titulo: "Crecer con vos",
      frase: "Cada caída tuvo tus manos cerca.",
      fotos: [
        { src: "fotos/04.jpg", texto: "El primer día de clases" },
        { src: "fotos/05.jpg" },
        { src: "fotos/06.jpg", texto: "Cumpleaños en casa" }
      ],
      golpe: "Nunca supimos cuánto te costaba. Vos hacías que pareciera fácil."
    },
    {
      titulo: "Las aventuras",
      frase: "Cualquier lugar era mejor si estabas.",
      fotos: [
        { src: "fotos/07.jpg", texto: "Ese viaje" },
        { src: "fotos/08.jpg" },
        { src: "fotos/09.jpg", texto: "Muertos de risa" },
        { src: "fotos/10.jpg" }
      ],
      golpe: "Las mejores historias de nuestra vida te tienen a vos de fondo."
    },
    {
      titulo: "Lo que no se ve",
      frase: "Las noches sin dormir. Los «avisame cuando llegás». El cansancio que te guardabas.",
      fotos: [
        { src: "fotos/11.jpg" },
        { src: "fotos/12.jpg" },
        { src: "fotos/13.jpg" }
      ],
      golpe: "Todo eso también era amor. Y lo vimos, ma. Lo vimos todo."
    },
    {
      titulo: "Hoy",
      frase: "Crecimos, pero seguimos volviendo a vos.",
      fotos: [
        { src: "fotos/14.jpg", texto: "Ahora" },
        { src: "fotos/15.jpg" },
        { src: "fotos/16.jpg", texto: "Siempre juntos" }
      ],
      golpe: "Todo lo que somos tiene algo tuyo."
    }
  ],

  // El final
  cierre: {
    titulo: "Feliz día, ma",
    mensaje: "Gracias por bancarnos siempre, incluso cuando no era fácil. Te queremos más de lo que sabemos decir.",
    firma: "Tus hijos"
  }
};
