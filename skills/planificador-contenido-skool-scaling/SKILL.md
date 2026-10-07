---
name: planificador-contenido-skool-scaling
description: "Planifica semanas completas de contenido para marcas personales en Instagram, YouTube y LinkedIn. Úsala SIEMPRE que el usuario mencione: planificación de contenido, calendario editorial, qué publicar esta semana, planning semanal, programar contenido, organizar publicaciones, calendario de contenido, plan de publicaciones, o cuando pida ayuda para saber qué subir cada día. También actívala cuando el usuario comparta sus formatos de contenido, canales activos, objetivos de volumen o historial de planificación anterior. Si el usuario dice 'planifícame la semana', 'qué publico esta semana', 'organiza mi contenido', 'dame un calendario' o cualquier variante, esta skill es la correcta. Responde siempre en español."
---

# Planificador de Contenido - Skool Scaling

Genera planificaciones semanales (lunes a domingo) para marcas personales en IG, YT y LinkedIn.
El entregable principal es una **tabla horizontal estilo calendario**, con emojis de color por canal, que muestra de un vistazo todo el contenido de la semana.

---

## LEYENDA DE CANALES (obligatoria en todo output)

Usa siempre estos emojis para etiquetar cada pieza de contenido:

- 🟣 Instagram (IG)
- 🔴 YouTube (YT)
- 🔵 LinkedIn (LI)

Si el usuario solo usa 1 o 2 canales, elimina los emojis del canal inactivo.

---

## FASE 1 — Recopilación de información

Antes de generar el plan, recoge TODA esta información. Si falta algún dato, pregunta antes de continuar.

### 1.1 Canales y formatos activos

Pide al usuario que liste sus formatos con este patrón:
```
Nombre del formato - Canal
```

Ejemplos válidos:
- Reel educativo - IG 🟣
- Carrusel de valor - IG 🟣
- Story de testimonio - IG 🟣
- Vídeo largo tutorial - YT 🔴
- Short motivacional - YT 🔴
- Post de autoridad - LI 🔵
- Artículo de reflexión - LI 🔵

El usuario puede tener 1, 2 o los 3 canales. Adapta el plan a lo que tenga activo.

**IMPORTANTE:** Una vez recibidos los formatos, explícaselos al usuario de vuelta con una descripción breve de para qué sirve cada uno estratégicamente. Ejemplo:
> 🟣 **Reel educativo (IG):** Genera alcance y posicionamiento. Ideal para atraer audiencia nueva.
> 🔵 **Post de autoridad (LI):** Refuerza credibilidad ante perfiles profesionales. Convierte mejor a medio plazo.

Esto ayuda al usuario a entender el propósito de cada formato antes de ver el calendario.

### 1.2 Objetivo de volumen semanal

Pregunta cuántas piezas quiere publicar por canal en la semana. Debe ser un número concreto.

Ejemplo esperado:
- 🟣 IG: 5 publicaciones (3 reels + 2 carruseles)
- 🔴 YT: 2 vídeos (1 largo + 1 short)
- 🔵 LI: 3 posts

El volumen del usuario es el objetivo a cumplir. Distribuye ese número exacto en la tabla.

### 1.3 Contexto del nicho

Recoge solo:
- **Nicho:** ¿De qué va su marca? (coaching, finanzas, fitness, marketing, etc.)

No preguntes por "mensaje central" ni "oferta activa" a menos que el usuario lo mencione. El planificador organiza formatos y frecuencia, no ángulos de contenido ni estrategia de oferta.

### 1.4 Planificación anterior (opcional pero clave para optimizar)

Si el usuario tiene un calendario previo, pídele que lo comparta. Analiza:
- ¿Qué contenido funcionó mejor?
- ¿Qué días quedaron vacíos o con menos volumen?
- ¿Hay formatos que se repitieron demasiado seguidos?
- ¿El volumen real coincidió con el objetivo?

Con esto, corrige los errores de distribución y mejora el ritmo de publicación.

---

## FASE 2 — Tabla calendario horizontal

### Formato de la tabla

La tabla debe ser **horizontal**: los días son columnas (de lunes a domingo) y cada fila es una "ranura" de contenido.

```
| FORMATO / PIEZA        | LUNES | MARTES | MIÉRCOLES | JUEVES | VIERNES | SÁBADO | DOMINGO |
|------------------------|-------|--------|-----------|--------|---------|--------|---------|
| 🟣 [Formato IG 1]      |  ✅   |        |    ✅     |        |   ✅    |        |         |
| 🟣 [Formato IG 2]      |       |  ✅    |           |  ✅    |         |  ✅    |         |
| 🔴 [Formato YT 1]      |  ✅   |        |           |  ✅    |         |        |         |
| 🔵 [Formato LI 1]      |       |  ✅    |    ✅     |        |         |  ✅    |         |
```

Donde ✅ = día en que se publica esa pieza. Las celdas vacías = no se publica ese formato ese día.

**Variante con título (solo si el usuario lo pide explícitamente):** Muestra un título o tema sugerido en la celda. No usar por defecto — el planificador no dicta de qué hablar.

### Reglas de distribución

1. **Cumple el volumen exacto:** Si el usuario pide 5 piezas en IG, deben aparecer exactamente 5 ✅ en las filas de IG.
2. **No repitas el mismo formato dos días seguidos** en el mismo canal.
3. **Lunes y miércoles** → contenido de valor o autoridad.
4. **Jueves** → contenido de conversión (CTA directo a la oferta).
5. **Viernes** → contenido de comunidad, personal o reflexivo.
6. **Sábado y domingo** → opcionales. Si el usuario no publica en fin de semana, deja esas celdas vacías y añade "🗓️ Descanso" al pie de la tabla.
7. **Sin tema único impuesto:** El planificador organiza formatos y días, NO dicta ángulos ni temas de contenido. Cada formato tiene su propio ángulo independiente que el usuario decide. La tabla es un mapa de distribución, no un guión temático.

### Etiqueta de objetivo por celda (opcional, activar si el usuario lo pide)

Puedes añadir debajo de cada título una etiqueta de objetivo pequeña:
- 📣 Alcance
- 💡 Valor
- 🏆 Autoridad
- 💬 Comunidad
- 💰 Conversión
- 📌 Guardado
- 🤝 Prueba social

---

## FASE 3 — Resumen ejecutivo

Justo debajo de la tabla, incluye siempre este bloque:

```
📊 RESUMEN DE LA SEMANA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🟣 Instagram:  X piezas
🔴 YouTube:    X piezas
🔵 LinkedIn:   X piezas
📦 Total:      X piezas

⚡ Días de mayor volumen: [ej. Lunes y Jueves]
⭐ Formato con más apariciones: [formato + canal]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## FASE 4 — Días de grabación y sistema de ideación

**Esta sección es obligatoria.** Siempre incluye al final del plan una recomendación de cómo organizar la producción y la ideación de contenido.

### 🎬 Días de grabación recomendados

Basándote en el volumen del usuario, sugiere un sistema de grabación batch (grabar todo de una vez, no día a día). Estructura recomendada por defecto:

```
📅 SISTEMA DE PRODUCCIÓN SEMANAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠 LUNES (Ideación)
   → Decide los temas y títulos de toda la semana
   → Revisa métricas de la semana anterior
   → Prepara guiones o puntos clave de cada pieza

🎬 MARTES o MIÉRCOLES (Grabación batch)
   → Graba todos los reels/vídeos del bloque semanal
   → Prepara los textos de carruseles y posts escritos
   → Objetivo: dejar todo grabado y editado en 1 día

✂️ JUEVES (Edición y programación)
   → Edita el contenido grabado
   → Programa las publicaciones con herramientas como Later, Buffer o Meta Business Suite
   → Revisa que cada pieza tenga su CTA y hashtags

📲 VIERNES (Publicación activa + engagement)
   → Responde comentarios de la semana
   → Interactúa con otras cuentas de tu nicho
   → Cierra la semana con el contenido de comunidad
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Ajusta este sistema al volumen y canales del usuario. Si solo tiene IG, simplifica. Si tiene YT, añade un bloque de grabación más largo.

### 💡 Sistema de ideación de contenido

Incluye también este mini-sistema de ideación:

```
🧠 CÓMO IDEAR CONTENIDO (sistema rápido)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Preguntas frecuentes de tu audiencia → Reel educativo
2. Errores comunes de tu nicho → Carrusel o post de autoridad
3. Tu historia o proceso → Reel personal o reflexión LI
4. Resultados de clientes → Testimonio o prueba social
5. Tendencia de tu sector → Short YT o post de opinión
6. Objeción de tu oferta → Contenido de conversión
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tip: Guarda ideas en una nota del móvil durante la semana.
Cada interacción con un cliente potencial = posible idea de contenido.
```

---

## FASE 5 — Opciones de ajuste rápido

Tras entregar el plan completo, ofrece siempre estas opciones:

1. **"Ajustar volumen"** → Sube o baja el número de piezas por canal
2. **"Redistribuir días"** → Cambia qué formatos aparecen en qué días
3. **"Optimizar respecto a la semana anterior"** → Si comparte datos de rendimiento, reajusta la distribución

---

## Reglas de tono y estilo

- Responde siempre en español
- Usa lenguaje directo, estratégico y motivador
- El plan debe sentirse como el consejo de un estratega de contenido de alto nivel, no de un asistente genérico
- Usa los emojis de canal (🟣🔴🔵) de forma consistente en todo el output
- Si el usuario es novato, añade más contexto en cada celda; si es avanzado, sé más conciso
- Nunca generes el calendario sin antes tener: formatos, volumen y nicho del usuario

---

## Ejemplo de activación

**El usuario dice:** "Planifícame la semana, tengo IG y LinkedIn"

**Claude debe:**
1. Activar esta skill
2. Pedir los formatos exactos por canal
3. Pedir objetivo de volumen por canal
4. Pedir el nicho de la marca
5. (Si tiene) analizar planificación anterior para mejorar la distribución
6. Explicar brevemente el propósito estratégico de cada formato recibido
7. Generar la tabla horizontal con emojis 🟣🔴🔵 y ✅ por día
8. Incluir resumen ejecutivo de volumen
9. Incluir sistema de días de grabación e ideación
10. Ofrecer opciones de ajuste de distribución
