# Sistema Visual — Skool Scaling

## Paleta base (variables CSS)

```css
:root {
  /* Colores de acento — REEMPLAZAR con brand kit del usuario */
  --blue:      #4e4fa3;   /* Primario: botones, tags, números, activo */
  --red:       #ba4849;   /* Acento: eyebrows, badges, alertas */
  --blue-lt:   #eeeef6;   /* Fondo tags azules, callouts informativos */
  --red-lt:    #f8eded;   /* Fondo badges rojos, callouts alerta */
  --blue-mid:  rgba(78,79,163,0.2);
  --red-mid:   rgba(186,72,73,0.2);

  /* Neutros — NO cambiar nunca */
  --dark:      #1e1e2e;   /* Títulos, énfasis fuerte */
  --mid:       #4a4a62;   /* Cuerpo, descripciones, listas */
  --light:     #9090b0;   /* Metadatos, labels, auxiliares */
  --bg:        #f7f7f5;   /* Fondo página, barras terminales */
  --white:     #ffffff;   /* Superficies de tarjetas */
  --border:    #e2e2ec;   /* Bordes de todos los elementos */
}
```

---

## Tipografía

```css
/* Importación obligatoria */
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

body {
  font-family: 'Inter', sans-serif;
  -webkit-font-smoothing: antialiased;
  background: var(--bg);
  color: var(--mid);
}
```

| Fuente | Uso | Peso | Tamaño |
|---|---|---|---|
| Instrument Serif | H1 display | 400/italic | clamp(36px, 5vw, 62px) |
| Inter | Cuerpo, labels, UI | 300/400/500/600 | 10–15px según jerarquía |
| JetBrains Mono | Labels sección, código, badges, nav tags | 400/500 | 8–12px, siempre uppercase |

**Regla H1:** línea 1 en dark, línea 2 siempre `<em>` italic con `color: var(--blue)` y guión largo `—`.

---

## Estructura obligatoria de documento

### 1 · NAV (height: 58px, sticky)

```html
<nav>
  <div class="nav-brand">
    <img src="[logo base64]" height="28" alt="Logo">
    <span class="nav-name">Nombre de Marca</span>
  </div>
  <span class="nav-tag">TIPO DE DOC</span>
</nav>
```

```css
nav {
  position: sticky; top: 0; z-index: 100;
  height: 58px; padding: 0 32px;
  display: flex; align-items: center; justify-content: space-between;
  background: var(--white); border-bottom: 1px solid var(--border);
}
.nav-name { font-weight: 600; color: var(--dark); font-size: 14px; }
.nav-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px; color: var(--blue); letter-spacing: 0.15em; text-transform: uppercase;
}
```

---

### 2 · HERO

```html
<div class="hero">
  <div class="eyebrow">TIPO DE HERRAMIENTA · CONTEXTO</div>
  <h1>Título del Documento<br><em>— Nombre de Marca</em></h1>
  <p class="subtitle">Descripción breve de lo que aprenderá el lector.</p>
  <div class="pills">
    <span class="pill pill-blue">CONCEPTO</span>
    <span class="pill pill-red">ACCIÓN</span>
    <span class="pill pill-blue">RESULTADO</span>
  </div>
</div>
```

```css
.hero {
  padding: 64px 40px 52px; text-align: center;
  background: var(--white); border-bottom: 1px solid var(--border);
}
.eyebrow {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px; color: var(--red); letter-spacing: 0.18em; text-transform: uppercase;
  margin-bottom: 20px;
}
.eyebrow::before, .eyebrow::after {
  content: ''; display: inline-block;
  width: 20px; height: 1px; background: var(--red);
  vertical-align: middle; margin: 0 10px;
}
h1 {
  font-family: 'Instrument Serif', serif;
  font-size: clamp(36px, 5vw, 56px);
  line-height: 1.1; letter-spacing: -0.01em;
  color: var(--dark); margin-bottom: 16px;
}
h1 em { color: var(--blue); font-style: italic; }
.subtitle { font-size: 15px; color: var(--light); max-width: 560px; margin: 0 auto 28px; }
.pills { display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; }
.pill {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px; letter-spacing: 0.12em; text-transform: uppercase;
  padding: 5px 12px; border-radius: 20px;
}
.pill-blue { background: var(--blue-lt); color: var(--blue); }
.pill-red  { background: var(--red-lt);  color: var(--red);  }
```

---

### 3 · STATS BAR (siempre 4 columnas)

```html
<div class="stats-bar">
  <div class="stat"><span class="stat-num">7</span><span class="stat-lbl">PASOS CLAVE</span></div>
  <div class="stat"><span class="stat-num">15 min</span><span class="stat-lbl">TIEMPO LECTURA</span></div>
  <div class="stat"><span class="stat-num">3x</span><span class="stat-lbl">MÁS CONVERSIÓN</span></div>
  <div class="stat"><span class="stat-num">100%</span><span class="stat-lbl">ACCIONABLE</span></div>
</div>
```

```css
.stats-bar {
  display: grid; grid-template-columns: repeat(4, 1fr);
  background: var(--white); border-bottom: 1px solid var(--border);
}
.stat {
  padding: 20px 24px; text-align: center;
  border-right: 1px solid var(--border);
  display: flex; flex-direction: column; gap: 4px;
}
.stat:last-child { border-right: none; }
.stat-num { font-size: 22px; font-weight: 700; color: var(--dark); }
.stat-lbl {
  font-family: 'JetBrains Mono', monospace;
  font-size: 8px; color: var(--light); letter-spacing: 0.14em; text-transform: uppercase;
}
```

---

### 4 · MAIN

```css
main {
  max-width: 900px; margin: 0 auto;
  padding: 52px 40px 100px;
}
.section { margin-bottom: 60px; }
```

---

### 5 · SECTION HEADER (obligatorio en cada sección)

```html
<div class="section-hd">
  <span class="s-num">00</span>
  <span class="s-title">TÍTULO DE SECCIÓN</span>
</div>
```

```css
.section-hd {
  display: flex; align-items: center; gap: 12px; margin-bottom: 24px;
}
.s-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px; color: var(--blue);
  background: var(--blue-lt); border: 1px solid var(--blue-mid);
  padding: 3px 9px; border-radius: 3px;
}
.s-title {
  font-size: 11px; font-weight: 600; color: var(--mid);
  text-transform: uppercase; letter-spacing: 0.1em;
}
.section-hd::after {
  content: ''; flex: 1; height: 1px; background: var(--border);
}
```

---

### 6 · FOOTER

```html
<footer>
  <div class="footer-brand">
    <img src="[logo base64]" height="24" alt="Logo">
    <span class="footer-name">Nombre de Marca</span>
  </div>
  <span class="footer-meta">DESCRIPCIÓN DEL RECURSO · nombredemarca.com</span>
</footer>
```

```css
footer {
  display: flex; align-items: center; justify-content: space-between;
  padding: 24px 40px; background: var(--white);
  border-top: 1px solid var(--border);
}
.footer-brand { display: flex; align-items: center; gap: 10px; }
.footer-name { font-weight: 600; font-size: 13px; color: var(--dark); }
.footer-meta {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px; color: var(--light); letter-spacing: 0.1em; text-transform: uppercase;
}
```
