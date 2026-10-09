---
name: metricas-instagram
description: Instagram reel tracking for Abel — n8n daily flow (Instagram API) → Google Sheet «Métricas Instagram · Abel»; I enrich rows (hook, format, belief) and write the weekly report
metadata:
  type: project
---

**Para qué (Abel, 09/10/2026):** «todo lo que no mides, no hay forma de saber si lo has hecho bien». Sirve para decidir de qué hacer más contenido.

**Cómo publica:** sube los reels a YouTube (con `programar_youtube.py` / n8n) y Repurpose.io los pasa a Instagram con el mismo título y descripción. Por eso la 1.ª línea del post = la 1.ª línea de nuestro `.txt`, y ahí se cruzan.

**Montaje:**
- Flujo: `herramientas/instagram/n8n_metricas_instagram.json` (pasos en el `LEEME.md` de esa carpeta).
- Hoja: Google Sheet «Métricas Instagram · Abel», id `1cTxkE86Py5Fn3uWBBHTKIxsaxWB3I5GbGkqrSoTKZXw`, pestaña `Reels`. Se lee y escribe con las herramientas de Google Sheets.
- **UNA VEZ POR SEMANA** (lunes 9:00). Diario no (Abel: «me voy a volver loco»).
- **Solo lo útil** (Abel 09/10/2026: demasiados datos le desvían). Columnas:
  - fecha, título, vistas, me_gusta, comentarios, compartidos, guardados, interacciones, segundos_vista;
  - **DMs**: separados de compartidos; lo que cuenta es que le escriban. La API no los da por reel: los pone él o me los dice;
  - **lectura**: la escribe SOLA el flujo y SOLO en los que destacan (Abel: «este sí, este sí», para tener foco). Si no destaca, va en blanco. Reglas en el nodo «Preparar fila», solo para reels de 3 días o más:
    - 🏆 EL MEJOR: vistas relativas + % guardados + % compartidos;
    - 👁 TOP VISTAS: los 3 primeros;
    - 💾 EL QUE MÁS SE GUARDA: con ≥1.000 vistas;
    - ✅ SÍ: ≥1.000 vistas y (guarda ≥4 % o ≥20 compartidos).
    El 09/10 salieron 9 de 39.
  - enlace, id.
- Token de Instagram: Instagram Login, 60 días. Lo pega él en n8n (nunca en el chat). Recordarle renovarlo.

**DMs (09/10/2026):** segundo flujo `herramientas/instagram/n8n_dms_instagram.json`. Un webhook de mensajes de Instagram apunta cada DM recibido en la pestaña «DMs»:
- fecha;
- persona_id (sin nombre);
- mensaje;
- reel_compartido.
Cada semana se atribuye cada DM a su reel: por el reel compartido, por el contenido del mensaje o por las 48 h siguientes a la publicación.

**Informe semanal en el móvil:** rutina de Claude en la nube, los lunes a las 09:00 UTC (después del n8n de las 9:00 de España). Instrucciones listas en `herramientas/instagram/rutina_claude_informe_semanal.md`. El 09/10 no se pudo crear desde aquí (el API de rutinas respondió «essential-traffic-only»): crearla desde claude.ai/code/routines con el conector de Google Sheets, o reintentarlo.

**Estado (09/10/2026):**
- Flujo de métricas funcionando: 39 reels con datos.
- Flujo de DMs funcionando de punta a punta: webhook verificado en Meta, campo `messages`, probado con el botón Test. El código acepta los dos formatos (entry.messaging real y entry.changes del Test).
- Faltan:
  - ✅ app PUBLICADA el 09/10, con la política de privacidad en Google Sites (contacto ester@abelgarciaf.com; texto en el Google Doc «Política de privacidad · Abel García»);
  - PENDIENTE la revisión de Meta (acceso avanzado) de `instagram_business_manage_messages`, con textos, guion del vídeo y respuestas en el Google Doc «Revisión de Meta · instagram_business_manage_messages». Sin eso solo llegan los DMs de cuentas con rol;
  - renovación automática del token (60 días);
  - crear la rutina de Claude del lunes.

**09/10/2026 · DMs SIN revisión de Meta.** La API ya deja leer las conversaciones y los mensajes completos con el token actual (`/me/conversations` + `/{id}?fields=messages{...}`). Nuevo flujo `herramientas/instagram/n8n_dms_semanal.json` (generado con `_hacer_dms_semanal.py`), los lunes a las 9:15:
- lee sus 40 reels y sus conversaciones;
- por cada conversación que EMPEZÓ otra persona escribe en «DMs»: primer mensaje, persona `u_id`, reel atribuido y cómo (compartido / 48h / sin reel);
- cuenta las conversaciones por reel y rellena la columna DMs de «Reels».
El flujo de webhook (`n8n_dms_instagram.json`) queda de sobra: se desactiva para no duplicar. La revisión de Meta ya no hace falta.

**Atribución interpretando el mensaje (Abel 09/10: «me sirve»).**
- Pestaña «DMs» con dos columnas más, `reel_final` y `como_final`, que escribe SOLO la rutina de Claude. n8n escribe A-G y no las toca.
- La rutina:
  - interpreta el mensaje (como_final = compartido / contenido / 48h / sin reel / no es lead);
  - recalcula la columna DMs de «Reels» (pisa el recuento de n8n de las 9:15);
  - deja el informe.
- Instrucciones listas en el Google Doc «Rutina de Claude · Informe semanal de Instagram», id `1OB2kvF1GRy05lu0xqJl0Cc53Nd9_BIUFEWPrgShiLaM`. Se ejecuta los lunes a las 11:00 en el entorno ABEL MARCA PERSONAL, con el conector de Google Sheets.
- La API de rutinas no estaba disponible desde la sesión («essential-traffic-only»): la crea él en claude.ai/code/routines.
- Sustituye a `herramientas/instagram/rutina_claude_informe_semanal.md`.

**09/10/2026 · La rutina se hizo LOCAL**, no en la nube: tarea programada `informe-semanal-instagram` de la app de escritorio, lunes a las 11:00, en `~/.claude/scheduled-tasks/informe-semanal-instagram/SKILL.md`. Solo se ejecuta con la app abierta; si está cerrada, se ejecuta al abrirla. Ni el Control remoto ni la API de rutinas en la nube funcionaron desde esta sesión.
Activé «Conectar sesiones nuevas al Control remoto» = On, para verlas en el móvil.
La rutina de «stories diarias» es de la nube: la tiene que borrar él en claude.ai/code/routines.
