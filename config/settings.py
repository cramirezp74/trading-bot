import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")
RSI_SOBREVENTA = float(os.getenv("RSI_SOBREVENTA", 30))
RSI_SOBRECOMPRA = float(os.getenv("RSI_SOBRECOMPRA", 70))
CANTIDAD = float(os.getenv("TRADE_AMOUNT", 50))
INTERVALO = os.getenv("TRADE_INTERVAL", "1h")
SIMULAR = os.getenv("SIMULATE_TRADES", "True").lower() == "true"

# Configuración de Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
