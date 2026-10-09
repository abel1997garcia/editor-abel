"""Genera n8n_dms_semanal.json (flujo semanal de DMs leyendo las conversaciones con la API) y prueba su código."""
import json, subprocess
YO = '17841415488505993'
dms = r'''// Una fila por CONVERSACIÓN que empezó otra persona: su primer mensaje y a qué reel se atribuye.
// compartido = te escribe compartiendo tu reel · 48h = empezó en las 48 h siguientes a un reel · sin reel
const YO = '__YO__';
const ms = s => Date.parse(String(s).replace('+0000', 'Z'));
const reels = $('Mis reels').all().map(i => i.json).flatMap(j => j.data || []).filter(m => m.media_product_type === 'REELS')
  .map(m => ({ id: 'ig_' + m.id, enlace: m.permalink, codigo: (m.permalink.match(/reel\/([^/]+)/) || [])[1], t: ms(m.timestamp) }))
  .sort((a, b) => b.t - a.t);
const out = [];
for (const it of $input.all()) {
  const c = it.json, msgs = (c.messages?.data || []).slice().sort((a, b) => ms(a.created_time) - ms(b.created_time));
  const primero = msgs[0]; if (!primero || primero.from?.id === YO) continue;              // la empezaste tú: no cuenta
  const t = ms(primero.created_time);
  const enlaces = msgs.filter(m => m.from?.id !== YO).flatMap(m => (m.shares?.data || []).map(s => s.link || ''));
  let reel = reels.find(r => r.codigo && enlaces.some(l => l.includes(r.codigo))), como = reel ? 'compartido' : '';
  if (!reel) { reel = reels.find(r => r.t <= t && t - r.t <= 48 * 3600e3); como = reel ? '48h' : 'sin reel'; }
  out.push({ json: { fecha: primero.created_time.slice(0, 16).replace('T', ' '), persona_id: 'u_' + primero.from?.id,
    mensaje: (primero.message || (enlaces.length ? '[comparte una publicación]' : '[adjunto]')).slice(0, 300),
    reel_compartido: enlaces[0] || '', reel_atribuido: reel ? reel.enlace : '', como, mid: c.id, _reel: reel ? reel.id : '' } });
}
return out;'''.replace('__YO__', YO)
cuenta = r'''// DMs por reel (conversaciones que empezaron gracias a ese reel) -> columna DMs de la pestaña Reels
const n = {};
for (const it of $('DMs de cada conversación').all()) if (it.json._reel) n[it.json._reel] = (n[it.json._reel] || 0) + 1;
const reels = $('Mis reels').all().map(i => i.json).flatMap(j => j.data || []).filter(m => m.media_product_type === 'REELS');
return reels.map(m => ({ json: { id: 'ig_' + m.id, DMs: n['ig_' + m.id] || 0 } }));'''
qa = {"authentication": "genericCredentialType", "genericAuthType": "httpQueryAuth"}
SHEET = {"__rl": True, "mode": "url", "value": "https://docs.google.com/spreadsheets/d/1cTxkE86Py5Fn3uWBBHTKIxsaxWB3I5GbGkqrSoTKZXw/edit"}
def http(nombre, url, params, x, extra=None):
    n = {"parameters": {"url": url, **qa, "sendQuery": True, "queryParameters": {"parameters": [{"name": k, "value": v} for k, v in params]}, "options": {}},
         "name": nombre, "type": "n8n-nodes-base.httpRequest", "typeVersion": 4.2, "position": [x, 0]}
    n.update(extra or {}); return n
def hoja(nombre, pestana, cols, clave, x):
    return {"parameters": {"operation": "appendOrUpdate", "documentId": SHEET, "sheetName": {"__rl": True, "mode": "name", "value": pestana},
            "columns": {"mappingMode": "defineBelow", "value": {c: "={{ $json.%s }}" % c for c in cols}, "matchingColumns": [clave]}, "options": {}},
            "name": nombre, "type": "n8n-nodes-base.googleSheets", "typeVersion": 4.5, "position": [x, 0]}
nodos = [
 {"parameters": {"rule": {"interval": [{"field": "weeks", "weeksInterval": 1, "triggerAtDay": [1], "triggerAtHour": 9, "triggerAtMinute": 15}]}}, "name": "Cada lunes 9:15", "type": "n8n-nodes-base.scheduleTrigger", "typeVersion": 1.2, "position": [0, 0]},
 http("Mis reels", "https://graph.instagram.com/me/media", [("fields", "id,permalink,timestamp,media_product_type"), ("limit", "40")], 220),
 http("Conversaciones", "https://graph.instagram.com/me/conversations", [("platform", "instagram"), ("fields", "updated_time"), ("limit", "60")], 440, {"executeOnce": True}),
 {"parameters": {"fieldToSplitOut": "data", "options": {}}, "name": "Una por una", "type": "n8n-nodes-base.splitOut", "typeVersion": 1, "position": [660, 0]},
 http("Mensajes", "=https://graph.instagram.com/{{ $json.id }}", [("fields", "messages.limit(50){message,from,created_time,shares}")], 880, {"onError": "continueRegularOutput"}),
 {"parameters": {"jsCode": dms}, "name": "DMs de cada conversación", "type": "n8n-nodes-base.code", "typeVersion": 2, "position": [1100, 0]},
 hoja("Google Sheets · DMs", "DMs", ["fecha", "persona_id", "mensaje", "reel_compartido", "reel_atribuido", "como", "mid"], "mid", 1320),
 {"parameters": {"jsCode": cuenta}, "name": "Contar DMs por reel", "type": "n8n-nodes-base.code", "typeVersion": 2, "position": [1540, 0], "executeOnce": True},
 hoja("Google Sheets · DMs por reel", "Reels", ["id", "DMs"], "id", 1760)]
orden = [n["name"] for n in nodos]
W = {"name": "DMs de Instagram (semanal) → Google Sheets (Abel)", "nodes": nodos,
     "connections": {a: {"main": [[{"node": b, "type": "main", "index": 0}]]} for a, b in zip(orden, orden[1:])},
     "settings": {"executionOrder": "v1", "timezone": "Europe/Madrid"}}
json.dump(W, open('n8n_dms_semanal.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# prueba del código con datos de ejemplo
prueba = r'''
const A = %s, B = %s;
const media = { json: { data: [
  { id: '1', permalink: 'https://www.instagram.com/reel/AAA/', timestamp: '2026-10-08T17:00:02+0000', media_product_type: 'REELS' },
  { id: '2', permalink: 'https://www.instagram.com/reel/BBB/', timestamp: '2026-09-20T20:57:23+0000', media_product_type: 'REELS' }] } };
const conv = [
  { json: { id: 'c1', messages: { data: [{ message: 'Hola, me encantó', from: { id: '55' }, created_time: '2026-10-09T10:00:00+0000' }] } } },
  { json: { id: 'c2', messages: { data: [{ message: '', from: { id: '66' }, created_time: '2026-10-01T10:00:00+0000', shares: { data: [{ link: 'https://www.instagram.com/reel/BBB/?igsh=x' }] } }] } } },
  { json: { id: 'c3', messages: { data: [{ message: 'ok', from: { id: '77' }, created_time: '2026-10-02T11:00:00+0000' }, { message: 'hola', from: { id: '%s' }, created_time: '2026-10-02T10:00:00+0000' }] } } }];
let outA = [];
const $ = n => ({ all: () => n === 'Mis reels' ? [media] : outA.map(j => ({ json: j })) });
outA = new Function('$', '$input', A)($, { all: () => conv }).map(x => x.json);
console.log(JSON.stringify(outA, null, 1));
console.log(JSON.stringify(new Function('$', '$input', B)($, { all: () => [] }).map(x => x.json)));
''' % (json.dumps(dms), json.dumps(cuenta), YO)
open('_prueba.js', 'w', encoding='utf-8').write(prueba)
print(subprocess.run(['node', '_prueba.js'], capture_output=True, text=True, encoding='utf-8').stdout or 'ERROR')
