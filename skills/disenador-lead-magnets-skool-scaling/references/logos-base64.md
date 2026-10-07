# Logos en Base64

## Cuándo usar cada logo

| Línea de producto | Color principal | Logo a usar |
|---|---|---|
| Skool Scaling | Azul #4d4fa9 | `logo-ss-blue` |
| Skool Accelerator | Rojo #d54647 | `logo-ss-red` |
| Marca personal del usuario | Brand kit del usuario | Logo del usuario en base64 o nombre en texto |

---

## Integrar logo del usuario

Si el usuario sube una imagen de su logo, conviértela a base64 usando:

```python
import base64
with open("logo.png", "rb") as f:
    b64 = base64.b64encode(f.read()).decode()
    src = f"data:image/png;base64,{b64}"
```

O en el entorno de bash_tool:

```bash
base64 -w 0 logo.png | sed 's/^/data:image\/png;base64,/'
```

---

## Si el usuario no tiene logo

Usa el nombre de la marca en texto con el color primario del brand kit:

```html
<!-- En nav -->
<div class="nav-brand">
  <div class="brand-monogram" style="background: var(--blue);">SS</div>
  <span class="nav-name">Nombre de Marca</span>
</div>
```

```css
.brand-monogram {
  width: 28px; height: 28px; border-radius: 6px;
  display: flex; align-items: center; justify-content: center;
  color: white; font-weight: 700; font-size: 11px; letter-spacing: 0.02em;
}
```

---

## Logos de Skool Scaling / Skool Accelerator

> Los logos oficiales de Skool Scaling y Skool Accelerator deben ser proporcionados por el usuario
> como archivos de imagen (.png con fondo transparente) y convertidos a base64 en el momento de
> construcción del documento.
>
> Si el usuario está trabajando en un proyecto de Skool Scaling o Skool Accelerator y no proporciona
> el logo, usa el monograma "SS" con el color de la línea correspondiente (azul #4d4fa9 para
> Skool Scaling, rojo #d54647 para Skool Accelerator) hasta que el usuario aporte el archivo.

### Para convertir el logo que el usuario suba como archivo de proyecto:

```bash
# El logo está en /mnt/project/ o /mnt/user-data/uploads/
base64 -w 0 /mnt/project/logo.png
```

Luego incrustar como:
```html
<img src="data:image/png;base64,[RESULTADO]" height="28" alt="Logo">
```
