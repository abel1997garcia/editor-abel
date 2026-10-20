---
name: copia-seguridad
description: Abel's full backup — private GitHub repo editor-abel (local clone C:\Users\Clap\editor-abel) kept in sync by actualizar_copia.py; USB zip with FOTOS MIAS; never include secrets
metadata:
  type: project
---

**Por qué (Abel, 09/10/2026):** «si este ordenador se me jode, me quedo sin nada». Quiere TODO en GitHub para poder instalarlo en otro ordenador, y un zip para USB.

**Cómo está montado:**
- **Repositorio privado:** https://github.com/abel1997garcia/editor-abel. Copia local en `C:\Users\Clap\editor-abel`.
- **`python actualizar_copia.py`:** deja el repo igual que el ordenador.
  - `--subir`: commit y push.
  - `--usb`: además crea `Escritorio\PAQUETE_EDICION_ABEL_<fecha>.zip`, que añade FOTOS MIAS (1,37 GB el 09/10).
- **Qué copia:**
  - Editor vídeos (sin vídeos ni renders), FÁBRICA, MUSICA, IMAGENES, MEDIUM ALLAN (solo código y textos) y logos;
  - `~/.claude/skills` (menos video-use, que es público);
  - las 3 memorias;
  - las tareas programadas.
- **`INSTALAR.md`** en la raíz del repo: el paso a paso para otro ordenador.

**NUNCA se suben:**
- `~/.claude/settings.json` (lleva un ANTHROPIC_AUTH_TOKEN y un proveedor externo; además tiene `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`, que es lo que bloquea el Control remoto y las rutinas en la nube);
- `youtube_config.json`;
- «CONTRASEÑAS INSTAGRAM.txt» del escritorio.
Antes de cada subida, buscar secretos (sk-, IGAA…, access_token=).

**How to apply:** al terminar cambios importantes (herramientas, skills, memoria), ejecutar `python actualizar_copia.py --subir` y decírselo. El zip del USB solo cuando lo pida.

**Kit del portátil (18/10):** `python herramientas/kit_portatil.py` → Escritorio/«KIT ABEL <fecha>» con 4 módulos (0_COMUN, 1_EDITOR_ABEL, 2_EDITOR_ALLAN, 3_FABRICA; cada editor con su memoria) + INSTALAR.bat (doble clic: winget + instalar.py, que coloca todo, arregla rutas si el usuario de Windows no es «Clap» e instala librerías). Plantillas del instalador en herramientas/kit/. Usa los filtros de actualizar_copia.py (sin secretos). Si Abel pide «el kit del portátil», regenerarlo así: `python herramientas/kit_portatil.py --sin-material` (lo vital; el 4_MATERIAL_PROPIO, decenas de GB, solo si lo pide). Último: Escritorio/KIT ABEL 2026-10-20 (1,8 GB).
