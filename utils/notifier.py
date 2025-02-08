import requests
from config.settings import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from config.logger import logger

def enviar_mensaje_telegram(mensaje):
    """Envía un mensaje de alerta a Telegram."""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        logger.warning("⚠️ No se configuró Telegram correctamente.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            logger.info("📩 Notificación enviada a Telegram con éxito.")
        else:
            logger.error(f"⚠️ Error enviando mensaje a Telegram: {response.text}")
    except Exception as e:
        logger.error(f"⚠️ Excepción al enviar mensaje a Telegram: {e}")
