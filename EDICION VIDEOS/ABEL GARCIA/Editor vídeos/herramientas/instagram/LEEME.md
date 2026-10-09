# Métricas de Instagram → Google Sheets

Cada LUNES a las 9:00, n8n lee tus reels de Instagram y apunta en la hoja «Métricas Instagram · Abel» (pestaña «Reels») solo lo útil: vistas, me gusta, comentarios, compartidos, guardados, interacciones y segundos de visualización media.

«DMs» (los que te escriben por ese reel; Instagram no lo da) la rellenas tú o me lo dices. «lectura» la escribo yo: qué ha funcionado en ese reel y si hay que mirarlo.

## Montarlo (una vez)
1. **Token de Instagram:** en tu app de developers.facebook.com → producto **Instagram** → «API setup with Instagram login» → añade tu cuenta → **Generate token**. Permisos: `instagram_business_basic` e `instagram_business_manage_insights`.
2. **En n8n:** Workflows → Import from file → `n8n_metricas_instagram.json`.
3. **Credencial del token:** en el nodo «Mis publicaciones» → Credential → crear **Query Auth**:
   - Name = `access_token`
   - Value = el token, pegado por ti (no me lo pases).
   Pon la misma credencial en el nodo «Métricas del reel».
4. **Credencial de Google:** en el nodo «Google Sheets · Reels», tu cuenta de Google (la misma que usas en n8n).
5. **Prueba:** «Execute workflow» y mira la hoja. Si va, actívalo.

## Ojo
- El token de Instagram caduca a los **60 días**: renuévalo antes en la misma pantalla (te lo recuerdo).
- Instagram no dice qué reel te trajo cada DM; lo más cercano es «compartidos».
- Los trial reels puede que no salgan en la API como los normales: lo vemos en la primera ejecución.

# DMs de Instagram → pestaña «DMs» (flujo `n8n_dms_instagram.json`)
Cada DM que te llega se apunta al momento: fecha, persona (solo su número de id, sin nombre), el mensaje y, si te comparte un reel, cuál. Cada semana Claude atribuye cada DM a su reel (por el reel compartido, por lo que dice o por la fecha) y rellena la columna DMs de la pestaña «Reels».

## Montarlo (una vez)
1. **En n8n:** importa `n8n_dms_instagram.json`.
   - En el nodo «¿Es Meta verificando?» cambia `PON_AQUI_TU_PALABRA_DE_VERIFICACION` por una palabra que inventes.
   - Pon tu cuenta de Google en el nodo de la hoja.
   - Activa el flujo y copia la **Production URL** del nodo «Instagram avisa».
2. **En tu app de Meta** → Instagram → «API setup with Instagram login» → **Configure webhooks**:
   - Callback URL = esa Production URL.
   - Verify token = tu palabra.
   - Suscríbete al campo **messages**.
   - En el token, añade también el permiso `instagram_business_manage_messages`.
3. **Prueba:** que alguien te escriba un DM y mira si aparece en la pestaña «DMs».
