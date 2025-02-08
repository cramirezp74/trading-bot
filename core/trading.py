# core/trading.py

from binance.client import Client
from config.settings import API_KEY, API_SECRET, SIMULAR, CANTIDAD
from strategies.combined_strategy import evaluar_mercado
from config.logger import logger
from utils.notifier import enviar_mensaje_telegram

client = Client(API_KEY, API_SECRET)

def comprar():
    try:
        logger.info("🟢 Intentando comprar BTC...")
        if SIMULAR:
            mensaje = f"✅ *Simulación:* Compra de ${CANTIDAD} USDT en BTC"
            logger.info(mensaje)
        else:
            order = client.order_market_buy(symbol="BTCUSDT", quoteOrderQty=CANTIDAD)
            mensaje = f"✅ *Orden de compra ejecutada:* {order}"
        enviar_mensaje_telegram(mensaje)
    except Exception as e:
        logger.error(f"⚠️ Error al comprar BTC: {e}")
        enviar_mensaje_telegram(f"⚠️ *Error al comprar BTC:* {e}")

def vender():
    try:
        logger.info("🔴 Intentando vender BTC...")
        if SIMULAR:
            mensaje = f"✅ *Simulación:* Venta de ${CANTIDAD} USDT en BTC"
            logger.info(mensaje)
        else:
            balance = client.get_asset_balance(asset="BTC")
            cantidad_btc = float(balance["free"])
            if cantidad_btc > 0:
                order = client.order_market_sell(symbol="BTCUSDT", quantity=cantidad_btc)
                mensaje = f"✅ *Orden de venta ejecutada:* {order}"
            else:
                mensaje = "⚠️ *No hay BTC suficiente para vender*"
        enviar_mensaje_telegram(mensaje)
    except Exception as e:
        logger.error(f"⚠️ Error al vender BTC: {e}")
        enviar_mensaje_telegram(f"⚠️ *Error al vender BTC:* {e}")

def ejecutar_trading():
    try:
        accion = evaluar_mercado()
        if accion == "comprar":
            comprar()
        elif accion == "vender":
            vender()
        else:
            logger.info("📈 Manteniendo posición, sin operaciones en esta iteración.")
    except Exception as e:
        logger.error(f"⚠️ Error en la ejecución del trading: {e}")
        enviar_mensaje_telegram(f"⚠️ *Error en la ejecución del trading:* {e}")
