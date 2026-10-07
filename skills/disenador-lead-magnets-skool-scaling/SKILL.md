---
name: disenador-lead-magnets-skool-scaling
description: >
  Diseña lead magnets profesionales en HTML con branding personalizado para cualquier marca personal,
  aplicando el sistema visual de Skool Scaling. Úsala SIEMPRE que el usuario pida crear un lead magnet,
  recurso gratuito, freebie, guía descargable, checklist, auditoría, playbook, prompt interactivo o
  cualquier documento de captación de leads. También actívala cuando el usuario quiera crear un documento
  con su identidad visual, transformar contenido en un recurso profesional con su branding, o pida
  "hazme un doc con mi diseño", "crea un lead magnet para mi marca", "quiero un recurso para regalar
  a mis seguidores". Si hay un brand kit, colores o referencia visual y se pide crear algo de valor
  para entregar: esta es la skill. Responde siempre en español.
---

# Diseñador de Lead Magnets — Skool Scaling

## Objetivo

Transformar cualquier contenido o descripción en un lead magnet HTML de alta calidad, adaptado al
brand kit de cualquier marca personal, siguiendo el sistema visual de Skool Scaling.

El output siempre es un archivo `.html` completo, autocontenido, descargable y listo para publicar.

---

## Flujo de trabajo obligatorio

### PASO 1 — Recopilar inputs del usuario

Antes de crear nada, confirma que tienes estos 4 elementos. Si falta alguno, pídeselo al usuario:

1. **Contenido o tema** — ¿De qué trata el lead magnet? ¿Qué valor entrega?
2. **Brand kit** — Nombre de marca, colores principales (HEX), tipografías si las tiene
3. **Tipo de documento** — Ver sección "Tipos de documento" más abajo
4. **Referencia visual** (opcional pero ideal) — Imagen, captura o descripción del estilo deseado

> Si el usuario no tiene brand kit definido, trabaja con lo que tenga (aunque sea solo un color y
> un nombre de marca). Nunca bloquees la creación por falta de inputs perfectos.

---

### PASO 2 — Adaptar el sistema visual al brand kit del usuario

El sistema base es el de Skool Scaling (ver `references/sistema-visual.md`), pero **todos los
colores de acento se reemplazan por los colores del brand kit del usuario**.

#### Reglas de adaptación de color:

| Variable sistema | Qué reemplaza | Regla |
|---|---|---|
| `--blue` (primario) | Color principal del brand kit | Botones, tags, números, secciones activas |
| `--red` (acento) | Color secundario del brand kit (o versión más oscura del primario) | Eyebrows, badges, alertas |
| `--blue-lt` | Versión muy clara del color principal (opacity 10-15%) | Fondos de tags, callouts |
| `--red-lt` | Versión muy clara del color secundario (opacity 10-15%) | Fondos de badges |
| `--dark`, `--mid`, `--light`, `--bg`, `--white`, `--border` | Neutros — no cambiar | Se mantienen siempre igual |

**Si el usuario tiene un solo color:** usa ese color como `--blue` y genera el `--red` como una
versión más oscura (+20% saturación) del mismo color.

#### Reglas de adaptación de logo:

- Si el usuario proporciona un logo como imagen: incrustar en base64 en nav y footer
- Si no hay logo: usar solo el nombre de la marca en texto bold con el color principal
- Si el usuario menciona Skool Scaling o Skool Accelerator: usar los logos del sistema base
  (ver `references/logos-base64.md`)

---

### PASO 3 — Seleccionar tipo de documento

Lee el contenido y determina qué tipo encaja mejor. Explícaselo al usuario antes de construir.

**Tipo A — Prompt Interactivo**
- El entregable central ES un prompt copiable (para usar en Claude, ChatGPT, etc.)
- Incluye el componente Prompt Terminal obligatoriamente
- Ejemplos: auditoría IA, generador de copy, analizador de marca

**Tipo B — Framework o Playbook**
- Explica una metodología o proceso paso a paso
- Componente principal: fases en acordeón expandible
- Ejemplos: sistema de contenido, proceso de lanzamiento, método de ventas

**Tipo C — Lead Magnet o Guía de Valor** *(más común)*
- El contenido es el protagonista. Se consume directamente.
- Callouts en abundancia, secciones bien estructuradas
- Ejemplos: checklist, guía práctica, recurso de formación, mini-curso

**Tipo D — SOP o Documento Interno**
- Referencia interna de equipo o sistema
- Incluye demos de componentes y prompt maestro de replicación al final

---

### PASO 4 — Construir el HTML

Sigue la estructura estándar. **No se puede omitir ninguna de estas partes:**

```
1. NAV sticky
2. HERO
3. STATS BAR (4 columnas con métricas relevantes del documento)
4. MAIN (secciones numeradas desde 00)
5. FOOTER
```

Lee `references/sistema-visual.md` para las especificaciones técnicas completas de cada componente.

Lee `references/componentes-html.md` para el código HTML/CSS base de cada componente reutilizable.

---

### PASO 5 — Reglas de copy

- **H1 siempre en dos líneas.** Línea 1: nombre del documento (Instrument Serif, dark). Línea 2: `<em>` italic en color primario del brand — con guión largo: `— Nombre de Marca`
- **Eyebrow en rojo mono uppercase** con líneas decorativas `::before` y `::after`
- **Pills:** máx. 4, alternando color primario y secundario, texto mono uppercase
- **Stats bar:** exactamente 4 cifras con métricas reales del contenido
- **Sin emojis en UI** (solo en phase-icon y dentro del prompt terminal)
- **Tono directo, cercano, sin corporativismo.** Copy real en español, nunca lorem ipsum
- **Secciones numeradas desde 00**

---

### PASO 6 — Output y entrega

1. Guarda el archivo como `/mnt/user-data/outputs/lead-magnet-[nombre-marca].html`
2. Usa `present_files` para entregárselo al usuario
3. Incluye un resumen de 2-3 líneas de las decisiones de diseño tomadas

---

## Tipos de contenido que puedes recibir

El usuario puede darte el contenido en cualquiera de estos formatos:

- **Texto plano o bullet points** → estructúralo tú en secciones lógicas
- **PDF o documento existente** → extrae el contenido y elévalo visualmente
- **Solo un tema** → genera el contenido completo basándote en la audiencia y nicho indicados
- **Prompt o metodología** → conviértelo en Tipo A con terminal copiable
- **Checklist o lista** → conviértelo en Tipo C con callouts y restricciones

---

## Referencias de esta skill

- `references/sistema-visual.md` — Sistema de colores, tipografías, estructura y componentes
- `references/componentes-html.md` — Código HTML/CSS base de cada componente reutilizable
- `references/logos-base64.md` — Logos de Skool Scaling y Skool Accelerator en base64

---

## Checklist antes de entregar

Antes de presentar el archivo, verifica:

- [ ] Colores del brand kit aplicados correctamente en todas las variables CSS
- [ ] Logo/nombre de marca en nav y footer
- [ ] Estructura completa: nav → hero → stats → main → footer
- [ ] H1 en dos líneas con segunda línea en itálica y color primario
- [ ] Stats bar con exactamente 4 columnas
- [ ] Secciones numeradas desde 00
- [ ] Copy real en español (sin lorem ipsum)
- [ ] Archivo HTML autocontenido (sin dependencias externas salvo Google Fonts)
- [ ] Tipografías importadas: Instrument Serif + Inter + JetBrains Mono
