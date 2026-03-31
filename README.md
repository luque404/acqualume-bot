# AcquaLume Bot

Bot web simple para Shopify/Railway, pensado para responder preguntas frecuentes.

## Archivos principales
- `app.py`: backend Flask + frontend del widget
- `requirements.txt`: dependencias
- `Procfile`: arranque en Railway

## Deploy en Railway
1. Subí estos archivos a un repo de GitHub.
2. Conectá el repo en Railway.
3. Railway debería detectar el `Procfile` automáticamente.
4. Opcional: agregá variables de entorno.

## Variables opcionales
- `BRAND_NAME`
- `PRIMARY_COLOR`
- `SECONDARY_COLOR`
- `SUPPORT_EMAIL`
- `INSTAGRAM_URL`
- `WHATSAPP_NUMBER`

## Probar local
```bash
pip install -r requirements.txt
python app.py
```

## Embed en Shopify
Pegá antes de `</body>`:
```html
<script src="https://TU-DOMINIO.up.railway.app/widget.js" defer></script>
```
