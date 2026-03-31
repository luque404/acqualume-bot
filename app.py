from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import List

from flask import Flask, jsonify, request, render_template_string, Response

app = Flask(__name__)

# =========================
# Configuración básica
# =========================
BRAND_NAME = os.getenv("BRAND_NAME", "AcquaLume")
PRIMARY_COLOR = os.getenv("PRIMARY_COLOR", "#0f172a")
SECONDARY_COLOR = os.getenv("SECONDARY_COLOR", "#06b6d4")
SUPPORT_EMAIL = os.getenv("SUPPORT_EMAIL", "tienda.acqualume@hotmail.com")
INSTAGRAM_URL = os.getenv("INSTAGRAM_URL", "https://instagram.com/acqualume.detailing")
WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "")


@dataclass
class FAQ:
    key: str
    title: str
    answer: str
    keywords: List[str]


FAQS: List[FAQ] = [
    FAQ(
        key="colores",
        title="¿Funciona en todos los colores?",
        answer=(
            "Sí, funciona en todos los colores. El producto actúa sobre la capa superficial "
            "de la pintura, ayudando a eliminar rayones y marcas sin afectar el pigmento ni el "
            "acabado original del vehículo. Por eso es seguro para cualquier tonalidad y ayuda "
            "a mantener el brillo original."
        ),
        keywords=["color", "colores", "blanco", "negro", "gris", "rojo", "azul", "tono"],
    ),
    FAQ(
        key="rayones",
        title="¿Sirve para todo tipo de rayones?",
        answer=(
            "Está diseñado para rayones superficiales, es decir, los que afectan solo la capa "
            "transparente de la pintura. Gracias a sus microabrasivos finos, ayuda a suavizar "
            "los bordes del rayón y a nivelar la superficie para recuperar uniformidad y brillo. "
            "No repara daños profundos que lleguen a la pintura base o a la chapa."
        ),
        keywords=["rayon", "rayones", "profundo", "superficial", "chapa", "pintura", "marca"],
    ),
    FAQ(
        key="comprar",
        title="¿Cómo hago para comprar?",
        answer=(
            "Podés hacer tu compra directamente desde la tienda online. Elegís el producto, lo "
            "agregás al carrito, completás tus datos y finalizás el pago. Si necesitás ayuda durante "
            "la compra, escribinos y te guiamos."
        ),
        keywords=["comprar", "compra", "carrito", "pagar", "pago", "pedido", "tienda"],
    ),
    FAQ(
        key="llega",
        title="¿En cuánto llega?",
        answer=(
            "Una vez realizado el pedido, el plazo estimado de entrega es de 3 a 8 días hábiles, "
            "dependiendo de la zona, días feriados y la logística del transporte. La mayoría de los "
            "envíos llegan dentro de ese rango."
        ),
        keywords=["llega", "llegar", "demora", "dias", "días", "envio", "envío", "tiempo"],
    ),
    FAQ(
        key="no_llego",
        title="Mi pedido no llegó todavía",
        answer=(
            "Si tu pedido todavía no llegó, primero revisá el estado con tu número de seguimiento. "
            "Si figura 'En camino', significa que ya fue despachado y está en tránsito hacia tu dirección "
            "o sucursal. Si figura 'Pendiente de ingreso', puede ser que aún no se haya despachado o que el "
            "sistema todavía no se haya actualizado, algo que a veces tarda algunas horas. Si ves una demora "
            "mayor a la esperada, escribinos y te ayudamos a revisarlo."
        ),
        keywords=["no llegó", "no llego", "no me llegó", "seguimiento", "en camino", "pendiente de ingreso", "andreani"],
    ),
    FAQ(
        key="aplicar",
        title="¿Cómo se aplica?",
        answer=(
            "Para aplicarlo correctamente: 1) lavá y secá bien la superficie; trabajá a la sombra y con la pintura fría. "
            "2) agitá el envase antes de usar. 3) aplicá una pequeña cantidad sobre un aplicador de espuma o paño de microfibra. "
            "4) trabajá por secciones de aproximadamente 30x30 cm con presión moderada y movimientos uniformes. "
            "5) retirás el exceso con un paño limpio. Repetí si hace falta. 6) para un mejor acabado, podés finalizar con un pulimento fino o una protección como cera o sellador."
        ),
        keywords=["aplico", "aplicar", "uso", "usar", "como se usa", "cómo se usa", "pasos", "microfibra"],
    ),
]

QUICK_REPLIES = [faq.title for faq in FAQS]

GREETING = (
    f"Hola, soy el asistente virtual de {BRAND_NAME}. Puedo ayudarte con compras, envíos, "
    "aplicación del producto y consultas frecuentes."
)

FALLBACK = (
    "No encontré una respuesta exacta para eso. Si querés, escribinos por Instagram o email y te ayudamos personalmente."
)


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    replacements = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ñ": "n",
    }
    for a, b in replacements.items():
        text = text.replace(a, b)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def get_contact_lines() -> List[str]:
    lines = []
    if INSTAGRAM_URL:
        lines.append(f"Instagram: {INSTAGRAM_URL}")
    if SUPPORT_EMAIL:
        lines.append(f"Email: {SUPPORT_EMAIL}")
    if WHATSAPP_NUMBER:
        lines.append(f"WhatsApp: {WHATSAPP_NUMBER}")
    return lines


def find_best_faq(message: str) -> FAQ | None:
    text = normalize_text(message)
    best_faq = None
    best_score = 0

    for faq in FAQS:
        score = 0
        for keyword in faq.keywords:
            if normalize_text(keyword) in text:
                score += 2
        title_words = normalize_text(faq.title).split()
        score += sum(1 for w in title_words if len(w) > 3 and w in text)
        if score > best_score:
            best_score = score
            best_faq = faq

    return best_faq if best_score > 0 else None


def build_reply(message: str) -> str:
    msg = normalize_text(message)
    if msg in {"hola", "buenas", "buen dia", "buenos dias", "buenas tardes", "buenas noches"}:
        return GREETING

    faq = find_best_faq(message)
    if faq:
        return faq.answer

    contact_lines = get_contact_lines()
    contact_block = "\n".join(contact_lines) if contact_lines else ""
    return f"{FALLBACK}\n\n{contact_block}".strip()


@app.get("/")
def home():
    return render_template_string(HOME_HTML, brand_name=BRAND_NAME)


@app.get("/health")
def health():
    return jsonify({"ok": True, "service": BRAND_NAME})


@app.get("/config")
def config():
    return jsonify(
        {
            "brand_name": BRAND_NAME,
            "primary_color": PRIMARY_COLOR,
            "secondary_color": SECONDARY_COLOR,
            "quick_replies": QUICK_REPLIES,
            "instagram_url": INSTAGRAM_URL,
            "support_email": SUPPORT_EMAIL,
            "whatsapp_number": WHATSAPP_NUMBER,
        }
    )


@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    if not message:
        return jsonify({"reply": "Escribime tu consulta y te ayudo."}), 400

    reply = build_reply(message)
    return jsonify({"reply": reply})


@app.get("/widget")
def widget():
    return render_template_string(
        WIDGET_HTML,
        brand_name=BRAND_NAME,
        primary_color=PRIMARY_COLOR,
        secondary_color=SECONDARY_COLOR,
        instagram_url=INSTAGRAM_URL,
        support_email=SUPPORT_EMAIL,
        whatsapp_number=WHATSAPP_NUMBER,
    )


@app.get("/widget.js")
def widget_js():
    base_url = request.host_url.rstrip("/")
    script = WIDGET_JS.replace("__BASE_URL__", base_url)
    return Response(script, mimetype="application/javascript")


HOME_HTML = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ brand_name }} Bot</title>
  <style>
    body{font-family:Arial,Helvetica,sans-serif;margin:0;padding:40px;background:#f8fafc;color:#0f172a}
    .card{max-width:820px;margin:0 auto;background:white;border-radius:18px;padding:32px;box-shadow:0 10px 30px rgba(15,23,42,.08)}
    h1{margin-top:0}
    code{background:#e2e8f0;padding:2px 6px;border-radius:6px}
    .demo{margin-top:18px;padding:14px 16px;background:#ecfeff;border:1px solid #a5f3fc;border-radius:12px}
  </style>
</head>
<body>
  <div class="card">
    <h1>{{ brand_name }} Bot</h1>
    <p>La app está funcionando correctamente.</p>
    <div class="demo">
      <strong>Endpoints:</strong><br>
      <code>/health</code><br>
      <code>/widget</code><br>
      <code>/widget.js</code><br>
      <code>/chat</code>
    </div>
    <p>Para embeberlo en Shopify, pegá este script antes de <code>&lt;/body&gt;</code>:</p>
    <pre><code>&lt;script src="{{ request.host_url.rstrip('/') }}/widget.js" defer&gt;&lt;/script&gt;</code></pre>
  </div>
</body>
</html>
"""


WIDGET_HTML = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ brand_name }} Chat</title>
  <style>
    :root {
      --primary: {{ primary_color }};
      --secondary: {{ secondary_color }};
      --bg: #f8fafc;
      --text: #0f172a;
      --muted: #64748b;
      --border: #e2e8f0;
      --bubble-bot: #e0f2fe;
      --bubble-user: #0f172a;
    }
    *{box-sizing:border-box}
    body{margin:0;font-family:Arial,Helvetica,sans-serif;background:#fff;color:var(--text)}
    .chat{display:flex;flex-direction:column;height:100vh}
    .header{padding:14px 16px;background:linear-gradient(135deg,var(--primary),var(--secondary));color:#fff}
    .header-title{font-weight:700}
    .header-sub{font-size:13px;opacity:.95;margin-top:4px}
    .messages{flex:1;overflow:auto;padding:14px;background:var(--bg)}
    .msg{max-width:86%;padding:12px 14px;border-radius:16px;margin:8px 0;line-height:1.45;white-space:pre-wrap}
    .bot{background:var(--bubble-bot);border-top-left-radius:6px}
    .user{background:var(--bubble-user);color:#fff;margin-left:auto;border-top-right-radius:6px}
    .quick{padding:12px;background:#fff;border-top:1px solid var(--border);display:flex;gap:8px;flex-wrap:wrap}
    .quick button{border:none;border-radius:999px;padding:8px 12px;background:#e2e8f0;color:#0f172a;cursor:pointer;font-size:12px}
    .composer{display:flex;gap:8px;padding:12px;background:#fff;border-top:1px solid var(--border)}
    .composer input{flex:1;border:1px solid var(--border);border-radius:999px;padding:12px 14px;font-size:14px}
    .composer button{border:none;border-radius:999px;padding:12px 16px;background:var(--primary);color:#fff;font-weight:700;cursor:pointer}
    .footer{padding:10px 14px;font-size:12px;color:var(--muted);background:#fff;border-top:1px solid var(--border)}
    a{color:inherit}
  </style>
</head>
<body>
  <div class="chat">
    <div class="header">
      <div class="header-title">{{ brand_name }}</div>
      <div class="header-sub">Consultas frecuentes, compras y envíos</div>
    </div>

    <div id="messages" class="messages"></div>

    <div class="quick" id="quickReplies"></div>

    <div class="composer">
      <input id="messageInput" type="text" placeholder="Escribí tu consulta..." />
      <button id="sendBtn">Enviar</button>
    </div>

    <div class="footer">
      Si necesitás atención humana:
      {% if instagram_url %}<a href="{{ instagram_url }}" target="_blank" rel="noopener">Instagram</a>{% endif %}
      {% if support_email %} · <a href="mailto:{{ support_email }}">{{ support_email }}</a>{% endif %}
      {% if whatsapp_number %} · WhatsApp: {{ whatsapp_number }}{% endif %}
    </div>
  </div>

<script>
  const messagesEl = document.getElementById('messages');
  const quickRepliesEl = document.getElementById('quickReplies');
  const inputEl = document.getElementById('messageInput');
  const sendBtn = document.getElementById('sendBtn');

  function addMessage(text, who) {
    const el = document.createElement('div');
    el.className = 'msg ' + who;
    el.textContent = text;
    messagesEl.appendChild(el);
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  async function loadConfig() {
    const res = await fetch('/config');
    const config = await res.json();
    quickRepliesEl.innerHTML = '';
    config.quick_replies.forEach((item) => {
      const btn = document.createElement('button');
      btn.textContent = item;
      btn.onclick = () => sendMessage(item);
      quickRepliesEl.appendChild(btn);
    });
    addMessage(`Hola, soy el asistente virtual de ${config.brand_name}. ¿En qué puedo ayudarte?`, 'bot');
  }

  async function sendMessage(message) {
    const text = (message ?? inputEl.value).trim();
    if (!text) return;
    addMessage(text, 'user');
    inputEl.value = '';

    try {
      const res = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });
      const data = await res.json();
      addMessage(data.reply || 'Hubo un error al responder.', 'bot');
    } catch (err) {
      addMessage('Hubo un problema al responder. Intentá de nuevo en unos segundos.', 'bot');
    }
  }

  sendBtn.addEventListener('click', () => sendMessage());
  inputEl.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') sendMessage();
  });

  loadConfig();
</script>
</body>
</html>
"""


WIDGET_JS = r"""
(function () {
  if (window.__ACQUALUME_BOT_LOADED__) return;
  window.__ACQUALUME_BOT_LOADED__ = true;

  var baseUrl = "__BASE_URL__";

  var button = document.createElement('button');
  button.setAttribute('aria-label', 'Abrir chat');
  button.innerHTML = '💬';
  button.style.position = 'fixed';
  button.style.right = '20px';
  button.style.bottom = '20px';
  button.style.width = '60px';
  button.style.height = '60px';
  button.style.border = 'none';
  button.style.borderRadius = '999px';
  button.style.background = 'linear-gradient(135deg, #0f172a, #06b6d4)';
  button.style.color = '#fff';
  button.style.fontSize = '26px';
  button.style.cursor = 'pointer';
  button.style.boxShadow = '0 10px 30px rgba(2, 132, 199, .35)';
  button.style.zIndex = '999999';

  var frame = document.createElement('iframe');
  frame.src = baseUrl + '/widget';
  frame.style.position = 'fixed';
  frame.style.right = '20px';
  frame.style.bottom = '92px';
  frame.style.width = '380px';
  frame.style.maxWidth = 'calc(100vw - 24px)';
  frame.style.height = '620px';
  frame.style.maxHeight = 'calc(100vh - 120px)';
  frame.style.border = 'none';
  frame.style.borderRadius = '18px';
  frame.style.boxShadow = '0 15px 50px rgba(15, 23, 42, .18)';
  frame.style.overflow = 'hidden';
  frame.style.background = '#fff';
  frame.style.zIndex = '999998';
  frame.style.display = 'none';

  button.addEventListener('click', function () {
    frame.style.display = frame.style.display === 'none' ? 'block' : 'none';
  });

  document.body.appendChild(frame);
  document.body.appendChild(button);
})();
"""


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, debug=True)
