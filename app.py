from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

FAQ_RESPONSES = {
    "colores": """Sí, funciona en todos los colores 👍
Actúa sobre la capa superficial de la pintura, por lo que no afecta el color ni el brillo original del auto.

En la mayoría de los casos, los rayones leves mejoran mucho y la superficie vuelve a verse uniforme.

¿Querés saber si tu rayón es superficial?""",

    "rayones": """Funciona muy bien en rayones y marcas superficiales 👍

Si el rayón ya es profundo (se siente con la uña o llegó a la pintura base), ahí normalmente ya requiere otro tipo de solución.

Si no estás seguro, podés escribirnos a tienda.acqualume@hotmail.com y te ayudamos.""",

    "aplicacion": """Es bastante simple de usar 👇

1. Limpiá y secá bien la superficie (a la sombra)
2. Aplicá una pequeña cantidad en un paño
3. Trabajá en secciones con movimientos uniformes
4. Retirá el exceso con un paño limpio

En unos minutos ya podés ver resultados.

¿Querés tips según tu caso?""",

    "envio": """Los envíos suelen tardar entre 3 y 8 días hábiles 👍

En la mayoría de los casos llegan dentro de ese rango sin problema.""",

    "pedido": """Si figura como “En camino”, ya fue despachado 👍
Si dice “Pendiente de ingreso”, puede estar por actualizarse.

Si ves algo raro, escribinos a tienda.acqualume@hotmail.com y lo vemos con vos.""",

    "comprar": """Podés comprar directamente desde esta página 👍

Si tenés dudas antes de hacerlo, escribinos y te ayudamos."""
}

def get_response(message):
    msg = message.lower()

    if "color" in msg:
        return FAQ_RESPONSES["colores"]
    elif "rayon" in msg:
        return FAQ_RESPONSES["rayones"]
    elif "aplicar" in msg:
        return FAQ_RESPONSES["aplicacion"]
    elif "envio" in msg or "llega" in msg:
        return FAQ_RESPONSES["envio"]
    elif "pedido" in msg:
        return FAQ_RESPONSES["pedido"]
    elif "comprar" in msg or "precio" in msg or "quiero" in msg:
        return FAQ_RESPONSES["comprar"]
    else:
        return "Si tenés dudas, escribinos a tienda.acqualume@hotmail.com y te ayudamos."

@app.route("/")
def home():
    return "Bot funcionando"

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    response = get_response(user_message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run()
