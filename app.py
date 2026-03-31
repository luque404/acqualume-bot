from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
import requests
import json

app = Flask(__name__)
CORS(app)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

KNOWLEDGE_BASE = """
Sos el asistente virtual de AcquaLume, una marca de removedor de rayones para autos. Respondé siempre en español, de forma amable, clara y breve. Si no sabés algo, decí que lo consulten por Instagram @acqualume o por email.

=== INFORMACIÓN DEL PRODUCTO ===

PREGUNTA: ¿Funciona en todos los colores?
RESPUESTA: Sí, funciona en todos los colores. El producto actúa únicamente sobre la capa superficial de la pintura, eliminando rayones y marcas sin afectar el pigmento ni el acabado original del vehículo. Es seguro para cualquier tonalidad y mantiene el brillo original.

PREGUNTA: ¿Para qué tipo de rayones sirve? ¿Funciona para rayones profundos?
RESPUESTA: Está diseñado para rayones superficiales, los que afectan solo la capa transparente de la pintura (clear coat). Gracias a sus microabrasivos finos, penetra ligeramente en el rayón, suaviza los bordes y nivela la superficie. Los rayones se difuminan y la pintura recupera su uniformidad y brillo. No repara daños profundos que lleguen a la pintura base o la chapa, pero deja la superficie lisa y protegida.

PREGUNTA: ¿Cómo se aplica? ¿Cómo lo uso?
RESPUESTA: Para aplicarlo correctamente:
1. Lavá y secá bien la superficie. Trabajá siempre a la sombra y con la pintura fría.
2. Agitá el envase antes de usar. Aplicá una pequeña cantidad sobre un aplicador de espuma o paño de microfibra.
3. Trabajá por secciones de 30x30 cm con presión moderada y movimientos uniformes.
4. Retirá el exceso con un paño de microfibra limpio. Repetí si es necesario para rayones más marcados.
5. Para un acabado superior podés terminar con un pulimento fino o aplicar cera o sellador.

PREGUNTA: ¿Cómo compro? ¿Cómo hago para comprar?
RESPUESTA: Podés comprarlo directamente desde nuestra tienda online en topgadgetpro.com. Es fácil y rápido — elegís tu pack, completás tus datos y listo. Aceptamos tarjeta de crédito, débito y transferencia.

PREGUNTA: ¿Cuánto tarda en llegar? ¿En cuánto llega?
RESPUESTA: Una vez realizado el pedido, llega en 3 a 8 días hábiles dependiendo de tu zona, días feriados y la logística de Andreani. La mayoría de los envíos llegan dentro de ese rango.

PREGUNTA: Mi pedido no llegó, ¿qué hago?
RESPUESTA: Primero verificá el estado del envío con el número de seguimiento que te enviamos por email.
- Si dice "En camino": el paquete ya fue despachado y está en tránsito, solo queda esperar.
- Si dice "Pendiente de ingreso": puede que aún no se haya despachado o que el sistema tarde en actualizarse (esto puede tardar varias horas).
Si después de esto hay algún problema o demora, contactanos por Instagram o email y lo solucionamos rápido.

PREGUNTA: ¿Tienen garantía? ¿Qué pasa si no funciona?
RESPUESTA: Sí, si el producto no da los resultados esperados en rayones superficiales, contactanos y buscamos la mejor solución para vos. Tu satisfacción es lo más importante.

INSTRUCCIONES GENERALES:
- Si preguntan por precio, deciles que entren a topgadgetpro.com para ver los packs disponibles.
- Si preguntan algo que no sabés, derivalos a Instagram @acqualume.
- Nunca inventes información que no esté en esta base de conocimiento.
- Respondé siempre en español rioplatense (vos, hacés, etc.)
- Sé breve y directo — máximo 3-4 líneas por respuesta salvo que sea necesario más.
"""

def get_ai_response(user_message, conversation_history):
    if not ANTHROPIC_API_KEY:
        return "Hola! Por el momento nuestro chat está en mantenimiento. Escribinos por Instagram @acqualume 😊"
    
    try:
        messages = conversation_history + [{"role": "user", "content": user_message}]
        
        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-haiku-4-5-20251001",
                "max_tokens": 300,
                "system": KNOWLEDGE_BASE,
                "messages": messages
            },
            timeout=10
        )
        return r.json()["content"][0]["text"]
    except Exception as e:
        return "Ups, algo salió mal. Escribinos por Instagram @acqualume y te ayudamos enseguida 😊"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    history = data.get("history", [])
    
    if not user_message:
        return jsonify({"error": "Mensaje vacío"}), 400
    
    response = get_ai_response(user_message, history)
    return jsonify({"response": response})

@app.route("/widget.js")
def widget_js():
    base_url = request.host_url.rstrip('/')
    js_code = f"""
(function() {{
  var CHAT_URL = '{base_url}';
  
  // Inject styles
  var style = document.createElement('style');
  style.textContent = `
    #acqualume-chat-btn {{
      position: fixed;
      bottom: 24px;
      right: 24px;
      width: 60px;
      height: 60px;
      border-radius: 50%;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
      border: 2px solid #00d4ff;
      cursor: pointer;
      z-index: 9999;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 20px rgba(0, 212, 255, 0.3);
      transition: all 0.3s ease;
    }}
    #acqualume-chat-btn:hover {{
      transform: scale(1.1);
      box-shadow: 0 6px 30px rgba(0, 212, 255, 0.5);
    }}
    #acqualume-chat-btn svg {{
      width: 28px;
      height: 28px;
      fill: #00d4ff;
    }}
    #acqualume-chat-window {{
      position: fixed;
      bottom: 100px;
      right: 24px;
      width: 360px;
      height: 500px;
      background: #0d0d1a;
      border: 1px solid #00d4ff33;
      border-radius: 16px;
      z-index: 9998;
      display: none;
      flex-direction: column;
      overflow: hidden;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }}
    #acqualume-chat-window.open {{
      display: flex;
    }}
    #acqualume-chat-header {{
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
      border-bottom: 1px solid #00d4ff33;
      padding: 16px 20px;
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    #acqualume-chat-header .avatar {{
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: linear-gradient(135deg, #00d4ff, #0099cc);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
    }}
    #acqualume-chat-header .info h4 {{
      margin: 0;
      color: #fff;
      font-size: 14px;
      font-weight: 600;
    }}
    #acqualume-chat-header .info span {{
      color: #00d4ff;
      font-size: 11px;
    }}
    #acqualume-chat-close {{
      margin-left: auto;
      background: none;
      border: none;
      color: #666;
      cursor: pointer;
      font-size: 20px;
      line-height: 1;
      padding: 0;
    }}
    #acqualume-chat-messages {{
      flex: 1;
      overflow-y: auto;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      scrollbar-width: thin;
      scrollbar-color: #333 transparent;
    }}
    .acq-msg {{
      max-width: 80%;
      padding: 10px 14px;
      border-radius: 12px;
      font-size: 13px;
      line-height: 1.5;
      animation: fadeIn 0.2s ease;
    }}
    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(8px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    .acq-msg.bot {{
      background: #1a1a2e;
      border: 1px solid #00d4ff22;
      color: #e0e0e0;
      align-self: flex-start;
      border-bottom-left-radius: 4px;
    }}
    .acq-msg.user {{
      background: linear-gradient(135deg, #00d4ff, #0099cc);
      color: #0d0d1a;
      align-self: flex-end;
      border-bottom-right-radius: 4px;
      font-weight: 500;
    }}
    .acq-msg.typing {{
      background: #1a1a2e;
      border: 1px solid #00d4ff22;
      color: #666;
      align-self: flex-start;
    }}
    #acqualume-chat-input-area {{
      padding: 12px 16px;
      border-top: 1px solid #00d4ff22;
      display: flex;
      gap: 8px;
    }}
    #acqualume-chat-input {{
      flex: 1;
      background: #1a1a2e;
      border: 1px solid #00d4ff33;
      border-radius: 24px;
      padding: 10px 16px;
      color: #fff;
      font-size: 13px;
      outline: none;
      transition: border-color 0.2s;
    }}
    #acqualume-chat-input:focus {{
      border-color: #00d4ff;
    }}
    #acqualume-chat-input::placeholder {{
      color: #444;
    }}
    #acqualume-chat-send {{
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: linear-gradient(135deg, #00d4ff, #0099cc);
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s;
      flex-shrink: 0;
    }}
    #acqualume-chat-send:hover {{
      transform: scale(1.1);
    }}
    #acqualume-chat-send svg {{
      width: 16px;
      height: 16px;
      fill: #0d0d1a;
    }}
    .acq-quick-btns {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-top: 4px;
    }}
    .acq-quick-btn {{
      background: #1a1a2e;
      border: 1px solid #00d4ff44;
      color: #00d4ff;
      padding: 5px 10px;
      border-radius: 20px;
      font-size: 11px;
      cursor: pointer;
      transition: all 0.2s;
      white-space: nowrap;
    }}
    .acq-quick-btn:hover {{
      background: #00d4ff;
      color: #0d0d1a;
    }}
  `;
  document.head.appendChild(style);

  // Create button
  var btn = document.createElement('div');
  btn.id = 'acqualume-chat-btn';
  btn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/></svg>';
  document.body.appendChild(btn);

  // Create window
  var win = document.createElement('div');
  win.id = 'acqualume-chat-window';
  win.innerHTML = `
    <div id="acqualume-chat-header">
      <div class="avatar">💧</div>
      <div class="info">
        <h4>AcquaLume</h4>
        <span>● En línea ahora</span>
      </div>
      <button id="acqualume-chat-close">×</button>
    </div>
    <div id="acqualume-chat-messages"></div>
    <div id="acqualume-chat-input-area">
      <input id="acqualume-chat-input" type="text" placeholder="Escribí tu consulta..." />
      <button id="acqualume-chat-send">
        <svg viewBox="0 0 24 24"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
      </button>
    </div>
  `;
  document.body.appendChild(win);

  var messages = document.getElementById('acqualume-chat-messages');
  var input = document.getElementById('acqualume-chat-input');
  var history = [];
  var isOpen = false;

  function addMessage(text, type) {{
    var msg = document.createElement('div');
    msg.className = 'acq-msg ' + type;
    msg.textContent = text;
    messages.appendChild(msg);
    messages.scrollTop = messages.scrollHeight;
    return msg;
  }}

  function addQuickButtons() {{
    var container = document.createElement('div');
    container.className = 'acq-quick-btns';
    var questions = ['¿Funciona en mi color?', '¿Para qué rayones sirve?', '¿Cómo lo aplico?', '¿Cuánto tarda?'];
    questions.forEach(function(q) {{
      var btn = document.createElement('button');
      btn.className = 'acq-quick-btn';
      btn.textContent = q;
      btn.onclick = function() {{
        sendMessage(q);
        container.remove();
      }};
      container.appendChild(btn);
    }});
    messages.appendChild(container);
    messages.scrollTop = messages.scrollHeight;
  }}

  function sendMessage(text) {{
    if (!text.trim()) return;
    addMessage(text, 'user');
    input.value = '';
    history.push({{role: 'user', content: text}});
    
    var typing = addMessage('...', 'typing');
    
    fetch(CHAT_URL + '/chat', {{
      method: 'POST',
      headers: {{'Content-Type': 'application/json'}},
      body: JSON.stringify({{message: text, history: history.slice(-6)}})
    }})
    .then(r => r.json())
    .then(data => {{
      typing.remove();
      var response = data.response || 'Ups, algo salió mal. Escribinos por Instagram.';
      addMessage(response, 'bot');
      history.push({{role: 'assistant', content: response}});
    }})
    .catch(() => {{
      typing.remove();
      addMessage('Ups, algo salió mal. Escribinos por Instagram @acqualume 😊', 'bot');
    }});
  }}

  function openChat() {{
    isOpen = true;
    win.classList.add('open');
    if (messages.children.length === 0) {{
      addMessage('¡Hola! 👋 Soy el asistente de AcquaLume. ¿En qué puedo ayudarte?', 'bot');
      addQuickButtons();
    }}
    input.focus();
  }}

  function closeChat() {{
    isOpen = false;
    win.classList.remove('open');
  }}

  btn.addEventListener('click', function() {{
    isOpen ? closeChat() : openChat();
  }});

  document.getElementById('acqualume-chat-close').addEventListener('click', closeChat);

  document.getElementById('acqualume-chat-send').addEventListener('click', function() {{
    sendMessage(input.value);
  }});

  input.addEventListener('keypress', function(e) {{
    if (e.key === 'Enter') sendMessage(input.value);
  }});
}})();
"""
    return js_code, 200, {'Content-Type': 'application/javascript'}

@app.route("/")
def index():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>AcquaLume Bot - Panel</title>
    <meta charset="utf-8">
    <style>
        body { font-family: -apple-system, sans-serif; background: #0d0d1a; color: #e0e0e0; padding: 40px; }
        h1 { color: #00d4ff; }
        .card { background: #1a1a2e; border: 1px solid #00d4ff33; border-radius: 12px; padding: 24px; margin: 20px 0; }
        code { background: #0d0d1a; border: 1px solid #333; padding: 4px 8px; border-radius: 4px; color: #00d4ff; font-size: 13px; }
        pre { background: #0d0d1a; border: 1px solid #333; padding: 16px; border-radius: 8px; overflow-x: auto; }
        .status { color: #00ff88; font-weight: bold; }
    </style>
</head>
<body>
    <h1>💧 AcquaLume Bot</h1>
    <p class="status">✅ Bot activo y funcionando</p>
    
    <div class="card">
        <h2>Instalar en Shopify</h2>
        <p>Pegá este código en <strong>Tienda → Temas → Editar código → theme.liquid</strong>, justo antes de <code>&lt;/body&gt;</code>:</p>
        <pre><code>&lt;script src="{{ request.host_url }}widget.js"&gt;&lt;/script&gt;</code></pre>
    </div>
    
    <div class="card">
        <h2>Probar el chat ahora</h2>
        <p>El widget ya está activo en esta página — mirá la esquina inferior derecha 👇</p>
    </div>
</body>
</html>
""")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
