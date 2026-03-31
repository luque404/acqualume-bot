from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
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
    follow_ups: List[str] = field(default_factory=list)


FAQS: List[FAQ] = [
    FAQ(
        key="colores",
        title="¿Funciona en todos los colores?",
        answer=(
            "Sí, funciona en todos los colores 👍\n\n"
            "Actúa sobre la capa superficial de la pintura, por lo que no afecta el color ni el brillo original del auto.\n\n"
            "En la mayoría de los casos, los rayones leves mejoran mucho y la superficie vuelve a verse uniforme.\n\n"
            "Si querés, también te explico cómo darte cuenta rápido si tu rayón es superficial."
        ),
        keywords=["color", "colores", "blanco", "negro", "gris", "rojo", "azul", "tono"],
        follow_ups=["¿Sirve para mi rayón?", "¿Cómo se aplica?"],
    ),
    FAQ(
        key="rayones",
        title="¿Sirve para todo tipo de rayones?",
        answer=(
            "Funciona muy bien en rayones y marcas superficiales 👍\n\n"
            "Si el rayón ya es profundo (se siente bastante con la uña o llegó a la pintura base), ahí normalmente ya requiere otro tipo de solución.\n\n"
            "Una forma rápida de orientarte es esta 👇\n\n"
            "Si el rayón casi no se siente al pasar la uña, suele ser superficial y el producto puede ayudarte mucho 👍\n\n"
            f"Si no estás seguro, podés escribirnos a {SUPPORT_EMAIL} y te ayudamos con tu caso sin problema."
        ),
        keywords=["rayon", "rayones", "profundo", "superficial", "chapa", "pintura", "marca", "sirve para mi rayon"],
        follow_ups=["¿Cómo se aplica?", "¿Cómo hago para comprar?"],
    ),
    FAQ(
        key="comprar",
        title="¿Cómo hago para comprar?",
        answer=(
            "Podés comprar directamente desde esta misma página 👍\n\n"
            f"Si antes de hacerlo tenés alguna duda sobre el producto o sobre tu caso, escribinos a {SUPPORT_EMAIL} y te ayudamos."
        ),
        keywords=["comprar", "compra", "carrito", "pagar", "pago", "pedido", "tienda", "precio", "lo quiero", "me interesa"],
        follow_ups=["¿Sirve para mi rayón?", "¿En cuánto llega?"],
    ),
    FAQ(
        key="llega",
        title="¿En cuánto llega?",
        answer=(
            "Los envíos suelen tardar entre 3 y 8 días hábiles, dependiendo de la zona y la logística 👍\n\n"
            "La gran mayoría llega dentro de ese rango sin inconvenientes.\n\n"
            "Si ya hiciste tu compra, podés seguir el envío con tu número de seguimiento.\n\n"
            f"Si ves alguna demora o algo que no te cierra, escribinos a {SUPPORT_EMAIL} y lo vemos con vos."
        ),
        keywords=["llega", "llegar", "demora", "dias", "días", "envio", "envío", "tiempo", "cuando llega", "cuanto tarda"],
        follow_ups=["Mi pedido no llegó todavía", "¿Cómo hago para comprar?"],
    ),
    FAQ(
        key="no_llego",
        title="Mi pedido no llegó todavía",
        answer=(
            "Primero te recomiendo revisar el estado con el número de seguimiento 👇\n\n"
            "Si figura como ‘En camino’, significa que ya fue despachado y está en tránsito.\n"
            "Si aparece como ‘Pendiente de ingreso’, puede ser que todavía no se haya actualizado o que esté por despacharse.\n\n"
            f"Si ves alguna demora o algo raro, escribinos a {SUPPORT_EMAIL} y lo vemos con vos."
        ),
        keywords=["no llegó", "no llego", "no me llegó", "seguimiento", "en camino", "pendiente de ingreso", "andreani", "pedido no llego"],
        follow_ups=["¿En cuánto llega?", "Hablar por mail"],
    ),
    FAQ(
        key="aplicar",
        title="¿Cómo se aplica?",
        answer=(
            "Es bastante simple de usar 👇\n\n"
            "1. Limpiá y secá bien la superficie (siempre a la sombra y con la pintura fría)\n"
            "2. Aplicá una pequeña cantidad en un paño de microfibra o aplicador\n"
            "3. Trabajá en secciones chicas con movimientos uniformes\n"
            "4. Retirá el exceso con un paño limpio\n\n"
            "En unos minutos ya podés empezar a notar cómo mejora el rayón 👍\n\n"
            "Si querés, te doy algunos tips para sacarle el mejor resultado según tu caso."
        ),
        keywords=["aplico", "aplicar", "uso", "usar", "como se usa", "cómo se usa", "pasos", "microfibra"],
        follow_ups=["¿Sirve para mi rayón?", "¿Funciona en todos los colores?"],
    ),
    FAQ(
        key="seguimiento_mail",
        title="¿Cómo veo mi número de seguimiento?",
        answer=(
            "El número de seguimiento suele enviarse por mail unos días después de haber realizado la compra 👍\n\n"
            "Te recomendamos revisar también la carpeta de spam o promociones por si llegó ahí.\n\n"
            f"Si no lo encontrás o tenés alguna duda, podés escribirnos a {SUPPORT_EMAIL} y te lo pasamos."
        ),  
        keywords=["seguimiento", "numero", "tracking", "donde veo mi pedido", "codigo envio"],
        follow_ups=["Mi pedido no llegó todavía", "¿En cuánto llega?"],
    ),
    FAQ(
        key="envios_pais",
        title="¿Hacen envíos a todo el país?",
        answer=(
            "Sí, hacemos envíos a todo Argentina 🇦🇷\n\n"
            "Llegamos sin problema a cualquier provincia 👍\n\n"
            "Si querés, te cuento también cuánto tarda en llegar a tu zona."
        ),
        keywords=["envios", "envíos", "tucuman", "tucumán", "interior", "provincia", "envian", "envían", "a todo el pais", "argentina"],
        follow_ups=["¿En cuánto llega?", "¿Cómo hago para comprar?"],
    ),
    FAQ(
        key="no_funciona",
        title="¿Qué pasa si el producto no funciona?",
        answer=(
            "Si no te funciona como esperabas, escribinos y lo vemos juntos 👍\n\n"
            "Nos importa que te sirva, no que compres y listo.\n\n"
            f"Podés contactarnos a {SUPPORT_EMAIL} y te ayudamos con tu caso."
        ),
        keywords=["no funciona", "no me sirvio", "no sirve", "garantia", "garantía", "devolucion", "devolución"],
        follow_ups=["¿Sirve para mi rayón?", "¿Cómo se aplica?"],
    ),
    FAQ(
        key="rinde",
        title="¿Cuánto rinde una botella?",
        answer=(
            "Rinde bastante 👍\n\n"
            "Los 200ml alcanzan para varias aplicaciones, dependiendo del uso.\n\n"
            "Al ser poca cantidad por aplicación, suele durar bastante más de lo que parece."
        ),
        keywords=["rinde", "cuanto rinde", "cuanto dura", "cuantas aplicaciones", "contenido", "ml"],
        follow_ups=["¿Cómo se aplica?", "¿Sirve para mi rayón?"],
    ),
]

BASE_QUICK_REPLIES = [
    "¿Sirve para mi rayón?",
    "¿Cómo se aplica?",
    "Tengo un problema con mi pedido",
]

GREETING = (
    f"Hola, soy el asistente virtual de {BRAND_NAME}. Te ayudo con dudas sobre el producto, aplicación, compras y envíos."
)

FALLBACK = (
    f"No encontré una respuesta exacta para eso. Si querés, escribinos a {SUPPORT_EMAIL} y te ayudamos personalmente."
)

BUY_INTENT_KEYWORDS = {
    "quiero comprar",
    "lo quiero",
    "me interesa",
    "precio",
    "quiero",
    "comprarlo",
    "comprar",
}

RAYON_HELP_KEYWORDS = {
    "sirve para mi rayon",
    "sirve para mi rayón",
    "mi rayon",
    "mi rayón",
    "como saber si es superficial",
    "cómo saber si es superficial",
}

MAIL_INTENT_KEYWORDS = {
    "hablar por mail",
    "mail",
    "correo",
    "email",
    "contacto",
}

ORDER_PROBLEM_KEYWORDS = {
    "tengo un problema con mi pedido",
    "problema con mi pedido",
    "mi pedido",
}


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


def default_suggestions() -> List[str]:
    return BASE_QUICK_REPLIES.copy()


def find_best_faq(message: str) -> FAQ | None:
    text = normalize_text(message)
    best_faq = None
    best_score = 0

    for faq in FAQS:
        score = 0
        for keyword in faq.keywords:
            keyword_norm = normalize_text(keyword)
            if keyword_norm in text:
                score += 3
        title_words = normalize_text(faq.title).split()
        score += sum(1 for w in title_words if len(w) > 3 and w in text)
        if score > best_score:
            best_score = score
            best_faq = faq

    return best_faq if best_score > 0 else None


def build_reply(message: str) -> tuple[str, List[str]]:
    msg = normalize_text(message)

    if msg in {"hola", "buenas", "buen dia", "buenos dias", "buenas tardes", "buenas noches"}:
        return GREETING, default_suggestions()

    if any(keyword in msg for keyword in BUY_INTENT_KEYWORDS):
        return (
            "Perfecto 👍\n\n"
            "Podés comprarlo directamente desde esta misma página.\n\n"
            f"Si querés estar seguro antes de hacerlo, escribinos a {SUPPORT_EMAIL} y te ayudamos sin problema."
        ), ["¿Sirve para mi rayón?", "¿En cuánto llega?"]

    if any(keyword in msg for keyword in RAYON_HELP_KEYWORDS):
        return (
            "Una forma rápida de orientarte es esta 👇\n\n"
            "Si el rayón casi no se siente al pasar la uña, suele ser superficial y el producto puede ayudarte mucho.\n\n"
            "Si se siente bastante, ya es más profundo y probablemente necesite otro tipo de trabajo.\n\n"
            f"Si querés, también podés escribirnos a {SUPPORT_EMAIL} y te ayudamos con tu caso."
        ), ["¿Cómo se aplica?", "¿Funciona en todos los colores?"]

    if any(keyword in msg for keyword in MAIL_INTENT_KEYWORDS):
        return (
            f"Claro. Podés escribirnos a {SUPPORT_EMAIL} y te ayudamos personalmente."
        ), ["¿Sirve para mi rayón?", "Tengo un problema con mi pedido"]

    if any(keyword in msg for keyword in ORDER_PROBLEM_KEYWORDS):
        faq = next((f for f in FAQS if f.key == "no_llego"), None)
        if faq:
            return faq.answer, faq.follow_ups or default_suggestions()

    faq = find_best_faq(message)
    if faq:
        return faq.answer, faq.follow_ups or default_suggestions()

    return FALLBACK, default_suggestions()


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
            "quick_replies": default_suggestions(),
            "support_email": SUPPORT_EMAIL,
        }
    )


@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    if not message:
        return jsonify({"reply": "Escribime tu consulta y te ayudo.", "suggestions": default_suggestions()}), 400

    reply, suggestions = build_reply(message)
    return jsonify({"reply": reply, "suggestions": suggestions})


@app.get("/widget")
def widget():
    return render_template_string(
        WIDGET_HTML,
        brand_name=BRAND_NAME,
        primary_color=PRIMARY_COLOR,
        secondary_color=SECONDARY_COLOR,
        support_email=SUPPORT_EMAIL,
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
    .header{
        position: relative;
        padding:14px 16px;
        background:linear-gradient(135deg,var(--primary),var(--secondary));
        color:#fff
    }

    .close-btn{
        position:absolute;
        top:10px;
        right:12px;
        background:transparent;
        border:none;
        color:#fff;
        font-size:22px;
        cursor:pointer;
    }

    @media (max-width: 600px){
      .close-btn{
        font-size:26px;
      }
    }
    
    .header-title{font-weight:700}
    .header-sub{font-size:13px;opacity:.95;margin-top:4px}
    .messages{flex:1;overflow:auto;padding:14px;background:var(--bg)}
    .msg{max-width:86%;padding:12px 14px;border-radius:16px;margin:8px 0;line-height:1.45;white-space:pre-wrap}
    .bot{background:var(--bubble-bot);border-top-left-radius:6px}
    .user{background:var(--bubble-user);color:#fff;margin-left:auto;border-top-right-radius:6px}
    .quick{padding:12px;background:#fff;border-top:1px solid var(--border);display:flex;gap:8px;flex-wrap:wrap}
    .quick button{border:none;border-radius:999px;padding:8px 12px;background:#e2e8f0;color:#0f172a;cursor:pointer;font-size:12px}
    .composer{display:flex;gap:8px;padding:12px;background:#fff;border-top:1px solid var(--border)}
    .composer input{
      flex:1;
      border:1px solid var(--border);
      border-radius:999px;
      padding:12px 14px;
      font-size:16px;
    }
    .composer button{border:none;border-radius:999px;padding:12px 16px;background:var(--primary);color:#fff;font-weight:700;cursor:pointer}
    .footer{padding:10px 14px;font-size:12px;color:var(--muted);background:#fff;border-top:1px solid var(--border)}
    a{color:inherit}
  </style>
</head>
<body>
  <div class="chat">
    <div class="header">
        <button id="closeBtn" class="close-btn">✕</button>
        <div class="header-title">{{ brand_name }}</div>
        <div class="header-sub">Te ayudamos con dudas sobre el producto, aplicación y envíos</div>
    </div>

    <div id="messages" class="messages"></div>

    <div class="quick" id="quickReplies"></div>

    <div class="composer">
      <input id="messageInput" type="text" placeholder="Escribí tu consulta..." />
      <button id="sendBtn">Enviar</button>
    </div>

    <div class="footer">
      Si necesitás atención humana: <a href="mailto:{{ support_email }}">{{ support_email }}</a>
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

  function renderQuickReplies(items) {
    quickRepliesEl.innerHTML = '';
    (items || []).forEach((item) => {
      const btn = document.createElement('button');
      btn.textContent = item;
      btn.onclick = () => sendMessage(item);
      quickRepliesEl.appendChild(btn);
    });
  }

  async function loadConfig() {
    const res = await fetch('/config');
    const config = await res.json();
    renderQuickReplies(config.quick_replies || []);
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
      renderQuickReplies(data.suggestions || []);
    } catch (err) {
      addMessage('Hubo un problema al responder. Intentá de nuevo en unos segundos.', 'bot');
    }
  }

  sendBtn.addEventListener('click', () => sendMessage());
  inputEl.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') sendMessage();
  });

  loadConfig();
document.getElementById('closeBtn').addEventListener('click', function () {
  window.parent.postMessage('closeChat', '*');
});
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
  var label = document.createElement('div');
  label.innerText = '¿Dudas?';
  label.style.position = 'fixed';
  label.style.right = '20px';
  label.style.bottom = '82px';
  label.style.background = '#0f172a';
  label.style.color = '#fff';
  label.style.padding = '4px 10px';
  label.style.borderRadius = '999px';
  label.style.fontSize = '12px';
  label.style.fontWeight = '600';
  label.style.boxShadow = '0 6px 15px rgba(0,0,0,0.2)';
  label.style.zIndex = '999999';
  label.style.whiteSpace = 'nowrap';
  label.style.transform = 'translateX(10%)';
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
  var isOpen = frame.style.display === 'block';

  frame.style.display = isOpen ? 'none' : 'block';
  label.style.display = isOpen ? 'block' : 'none';
});

  document.body.appendChild(frame);
  document.body.appendChild(button);
  document.body.appendChild(label);

  window.addEventListener('message', function (event) {
    if (event.data === 'closeChat') {
      frame.style.display = 'none';
    }
});
})();
"""


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, debug=True)
