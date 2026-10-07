# Componentes HTML Reutilizables

## A · Step Card (Cómo usar)

```html
<div class="steps-grid">
  <div class="step-card">
    <div class="step-num">01</div>
    <div class="step-content">
      <div class="step-title">TÍTULO DEL PASO</div>
      <div class="step-desc">Descripción clara y accionable de qué hace el usuario en este paso.</div>
    </div>
  </div>
</div>
```

```css
.steps-grid { display: flex; flex-direction: column; gap: 8px; }
.step-card {
  display: grid; grid-template-columns: 48px 1fr;
  background: var(--white); border: 1px solid var(--border); border-radius: 8px;
  overflow: hidden;
}
.step-num {
  display: flex; align-items: center; justify-content: center;
  font-family: 'Instrument Serif', serif; font-style: italic;
  font-size: 20px; color: var(--blue);
  background: var(--blue-lt); border-right: 1px solid var(--border);
}
.step-content { padding: 14px 18px; }
.step-title {
  font-size: 12px; font-weight: 600; color: var(--dark);
  text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 4px;
}
.step-desc { font-size: 12px; color: var(--mid); line-height: 1.6; }
```

---

## B · Phase Accordion

```html
<div class="phase" onclick="this.classList.toggle('open')">
  <div class="phase-icon">🎯</div>
  <div class="phase-info">
    <div class="phase-tag">FASE 01</div>
    <div class="phase-title">Nombre de la Fase</div>
    <div class="phase-desc">Descripción breve visible siempre.</div>
    <div class="phase-body">
      <p>Contenido detallado que aparece al expandir. Puede incluir listas, callouts, etc.</p>
    </div>
  </div>
</div>
```

```css
.phase {
  display: grid; grid-template-columns: 56px 1fr;
  background: var(--white); border: 1px solid var(--border);
  border-radius: 8px; margin-bottom: 8px; cursor: pointer; overflow: hidden;
}
.phase-icon {
  display: flex; align-items: flex-start; justify-content: center;
  padding-top: 16px; font-size: 20px;
  background: var(--bg); border-right: 1px solid var(--border);
}
.phase-info { padding: 16px 20px; }
.phase-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 8px; color: var(--blue); letter-spacing: 0.18em;
  text-transform: uppercase; margin-bottom: 4px;
}
.phase-title { font-size: 13px; font-weight: 600; color: var(--dark); margin-bottom: 4px; }
.phase-desc  { font-size: 12px; color: var(--mid); line-height: 1.5; }
.phase-body  { display: none; margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--border); }
.phase.open .phase-body { display: block; }
```

---

## C · Prompt Terminal (solo Tipo A)

```html
<div class="terminal">
  <div class="terminal-bar">
    <div class="dots">
      <span style="background:#ff5f57"></span>
      <span style="background:#febc2e"></span>
      <span style="background:#28c840"></span>
    </div>
    <span class="term-file">prompt_v1.txt</span>
    <span class="badge-red">COPIAR Y USAR</span>
  </div>
  <div class="terminal-body" id="prompt-content">
    <span class="hl-sec">// ═══ CONTEXTO ═══</span>
    Eres un experto en <span class="hl-r">[NICHO DEL USUARIO]</span>.
    Tu tarea es <span class="hl-b">analizar y optimizar</span> lo siguiente:

    <span class="hl-sec-r">// ═══ INPUT DEL USUARIO ═══</span>
    <span class="hl-r">[PEGA AQUÍ TU CONTENIDO]</span>

    <span class="hl-g">// Instrucciones adicionales</span>
    Responde siempre en español. Sé <span class="hl-d">directo y accionable</span>.
  </div>
  <div class="copy-row">
    <span class="copy-hint">// selecciona todo el prompt y cópialo en Claude</span>
    <button onclick="copyPrompt()">
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/>
      </svg>
      Copiar prompt
    </button>
  </div>
</div>

<script>
function copyPrompt() {
  const el = document.getElementById('prompt-content');
  navigator.clipboard.writeText(el.innerText);
  const btn = document.querySelector('.copy-row button');
  btn.style.background = '#22a05a';
  btn.textContent = '¡Copiado!';
  setTimeout(() => {
    btn.style.background = 'var(--blue)';
    btn.innerHTML = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg> Copiar prompt';
  }, 2200);
}
</script>
```

```css
.terminal { border: 1px solid var(--border); border-radius: 10px; overflow: hidden; }
.terminal-bar {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 16px; background: var(--bg); border-bottom: 1px solid var(--border);
}
.dots { display: flex; gap: 6px; }
.dots span { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
.term-file {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px; color: var(--light); flex: 1;
}
.badge-red {
  font-family: 'JetBrains Mono', monospace;
  font-size: 8px; color: var(--red); background: var(--red-lt);
  padding: 2px 8px; border-radius: 3px; letter-spacing: 0.1em;
}
.terminal-body {
  padding: 36px 40px; background: var(--white);
  font-family: 'JetBrains Mono', monospace;
  font-size: 11.5px; line-height: 2.05; color: var(--mid);
  white-space: pre-wrap;
}
.hl-b  { color: var(--blue); font-weight: 500; }
.hl-r  { color: var(--red);  font-weight: 500; }
.hl-d  { color: var(--dark); font-weight: 600; }
.hl-g  { color: var(--light); }
.hl-sec   { display: block; color: var(--blue); border-bottom: 1px solid var(--blue-mid); padding-bottom: 4px; margin-bottom: 8px; }
.hl-sec-r { display: block; color: var(--red);  border-bottom: 1px solid var(--red-mid);  padding-bottom: 4px; margin-bottom: 8px; }
.copy-row {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 16px; background: var(--bg); border-top: 1px solid var(--border);
}
.copy-hint {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px; color: var(--light); letter-spacing: 0.08em;
}
.copy-row button {
  display: flex; align-items: center; gap: 6px;
  background: var(--blue); color: white;
  border: none; border-radius: 5px; padding: 7px 14px;
  font-size: 12px; font-weight: 600; cursor: pointer;
  transition: background 0.2s;
}
```

---

## D · Restriction Card (sí/no)

```html
<div class="restrictions">
  <div class="rest-col">
    <div class="rest-title">LO QUE SÍ FUNCIONA</div>
    <div class="rest-item"><span class="check">✓</span> Descripción de práctica correcta.</div>
    <div class="rest-item"><span class="check">✓</span> Otra práctica recomendada.</div>
  </div>
  <div class="rest-col">
    <div class="rest-title">LO QUE NO FUNCIONA</div>
    <div class="rest-item"><span class="cross">✕</span> Descripción de error común.</div>
    <div class="rest-item"><span class="cross">✕</span> Otro error a evitar.</div>
  </div>
</div>
```

```css
.restrictions { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.rest-col { background: var(--white); border: 1px solid var(--border); border-radius: 8px; padding: 20px; }
.rest-title {
  font-size: 10px; font-weight: 600; color: var(--dark);
  text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 12px;
}
.rest-item { font-size: 11px; color: var(--mid); line-height: 1.55; margin-bottom: 6px; }
.check { color: var(--blue); font-weight: 700; margin-right: 6px; }
.cross { color: var(--red);  font-weight: 700; margin-right: 6px; }
```

---

## E · Callout Box

```html
<!-- Callout informativo (azul) -->
<div class="callout callout-blue">
  <span class="callout-label">NOTA IMPORTANTE</span>
  <p>Texto del callout con información clave que el lector no debe perderse.</p>
</div>

<!-- Callout de alerta (rojo) -->
<div class="callout callout-red">
  <span class="callout-label">ATENCIÓN</span>
  <p>Advertencia o punto crítico que puede afectar el resultado.</p>
</div>
```

```css
.callout {
  padding: 16px 20px; border-radius: 6px; margin: 20px 0;
}
.callout-blue { background: var(--blue-lt); border-left: 3px solid var(--blue); }
.callout-red  { background: var(--red-lt);  border-left: 3px solid var(--red);  }
.callout-label {
  display: block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 8px; letter-spacing: 0.15em; text-transform: uppercase;
  margin-bottom: 6px;
}
.callout-blue .callout-label { color: var(--blue); }
.callout-red  .callout-label { color: var(--red);  }
.callout p { font-size: 13px; color: var(--mid); line-height: 1.7; margin: 0; }
```

---

## F · Deliverable Card (grid 3 columnas)

```html
<div class="deliverables">
  <div class="deliv-card">
    <div class="deliv-num">01</div>
    <div class="deliv-title">Nombre del entregable</div>
    <div class="deliv-desc">Descripción breve de qué es y para qué sirve.</div>
  </div>
</div>
```

```css
.deliverables { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.deliv-card {
  background: var(--white); border: 1px solid var(--border);
  border-radius: 8px; padding: 20px; position: relative; overflow: hidden;
  transition: transform 0.2s;
}
.deliv-card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0;
  height: 2.5px; background: var(--blue);
  transform: scaleX(0); transition: transform 0.2s; transform-origin: left;
}
.deliv-card:hover::before { transform: scaleX(1); }
.deliv-card:hover { transform: translateY(-2px); }
.deliv-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px; color: var(--light); letter-spacing: 0.12em; margin-bottom: 8px;
}
.deliv-title { font-size: 12px; font-weight: 600; color: var(--dark); margin-bottom: 6px; }
.deliv-desc  { font-size: 11px; color: var(--mid); line-height: 1.5; }
```
