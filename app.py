# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify

app = Flask(__name__)

FAQ_RESPONSES = {

    "colores": """Sí, funciona en todos los colores 👍  
Actúa sobre la capa superficial de la pintura, por lo que no afecta el color ni el brillo original del auto.

En la mayoría de los casos, los rayones leves mejoran mucho y la superficie vuelve a verse uniforme.

Si querés, también te explico cómo darte cuenta rápido si tu rayón es superficial.""",

    "rayones": """Funciona muy bien en rayones y marcas superficiales 👍  

Si el rayón ya es profundo (se siente bastante con la uña o llegó a la pintura base), ahí normalmente ya requiere otro tipo de solución.

Si no estás seguro, podés escribirnos a tienda.acqualume@hotmail.com y te ayudamos con tu caso sin problema.""",

    "aplicacion": """Es bastante simple de usar 👇  

1. Limpiá y secá bien la superficie (siempre a la sombra y con la pintura fría)  
2. Aplicá una pequeña cantidad en un paño de microfibra o aplicador  
3. Trabajá en secciones chicas con movimientos uniformes  
4. Retirá el exceso con un paño limpio  

En unos minutos ya podés empezar a notar cómo mejora el rayón 👍  

Si querés, te doy algunos tips para sacarle el mejor resultado según tu caso.""",

    "envio": """Los envíos suelen tardar entre 3 y 8 días hábiles, dependiendo de la zona y la logística 👍  

La gran mayoría llega dentro de ese rango sin inconvenientes.

Si ya hiciste tu compra, podés seguir el envío con tu número de seguimiento.

Si ves alguna demora o algo que no te cierra, escribinos a tienda.acqualume@hotmail.com y lo vemos con vos.""",

    "pedido": """Si figura como “En camino”, significa que ya fue despachado y está en tránsito 👍  
Si dice “Pendiente de ingreso”, puede ser que aún no se haya actualizado o esté por despacharse.

Si ves alguna demora o algo raro, escribinos a tienda.acqualume@hotmail.com y lo vemos con vos.""",

    "seguimiento": """El número de seguimiento suele enviarse por mail unos días después de haber realizado la compra 👍  

Te recomendamos revisar también la carpeta de spam o promociones por si llegó ahí.

Si no lo encontrás o tenés alguna duda, podés escribirnos a tienda.acqualume@hotmail.com y te lo pasamos.""",

    "comprar": """Podés comprar directamente desde esta misma página 👍  

Si tenés alguna duda antes de hacerlo, escribinos a tienda.acqualume@hotmail.com y te ayudamos."""
}


def get_response(message):
    msg = message.lower()

    if "color" in msg:
        return FAQ_RESPONSES["colores"]

    elif "rayon" in msg:
        return FAQ_RESPONSES["rayones"]

    elif "aplicar" in msg or "uso" in msg:
        return FAQ_RESPONSES["aplicacion"]

    elif "envio" in msg or "llega" in msg:
        return FAQ_RESPONSES["envio"]

    elif "no llego" in msg or "demora" in msg:
        return FAQ_RESPONSES["pedido"]

    elif "seguimiento" in msg or "numero" in msg or "tracking" in msg:
        return FAQ_RESPONSES["seguimiento"]

    elif "comprar" in msg or "precio" in msg or "quiero" in msg or "me interesa" in msg:
        return FAQ_RESPONSES["comprar"]

    else:
        return "Si tenés alguna duda, escribinos a tienda.acqualume@hotmail.com y te ayudamos sin problema."


@app.route("/")
def home():
    return "AcquaLume Bot funcionando"


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    response = get_response(user_message)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run()
