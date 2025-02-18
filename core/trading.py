# core/trading.py

from binance.client import Client
from config.settings import API_KEY, API_SECRET, SIMULAR, CANTIDAD, STOP_LOSS_PERCENTAGE, TAKE_PROFIT_PERCENTAGE
from strategies.combined_strategy import evaluar_mercado
from config.logger import logger
from utils.notifier import enviar_mensaje_telegram
from core.db import registrar_trade  # Función para registrar trades en MariaDB

client = Client(API_KEY, API_SECRET)

def ejecutar_orden_compra(stop_loss, take_profit):
    try:
        logger.info("Ejecutando orden de COMPRA en BTC...")
        if SIMULAR:
            mensaje = (f"Simulación: Comprar BTC por ${CANTIDAD} USDT | "
                       f"SL: {stop_loss:.2f}, TP: {take_profit:.2f}")
            logger.info(mensaje)
            enviar_mensaje_telegram(mensaje)
            registrar_trade("BTCUSDT", "BUY", CANTIDAD, 0, stop_loss, take_profit, status="SIMULATED")
            return
        # Ejecutar orden de compra de mercado
        order = client.order_market_buy(symbol="BTCUSDT", quoteOrderQty=CANTIDAD)
        cantidad_btc = float(order.get("executedQty", 0))
        mensaje = f"Orden de compra ejecutada: {order}"
        logger.info(mensaje)
        enviar_mensaje_telegram(mensaje)
        # Configurar orden OCO para SL y TP
        oco_order = client.create_oco_order(
            symbol="BTCUSDT",
            side=Client.SIDE_SELL,
            quantity=cantidad_btc,
            price=str(take_profit),
            stopPrice=str(stop_loss),
            stopLimitPrice=str(stop_loss * 0.99),
            stopLimitTimeInForce="GTC"
        )
        mensaje_oco = f"OCO SL/TP ejecutada: {oco_order}"
        logger.info(mensaje_oco)
        enviar_mensaje_telegram(mensaje_oco)
        # Calcular precio promedio de compra
        executed_qty = float(order.get("executedQty", 0))
        cummulative_quote_qty = float(order.get("cummulativeQuoteQty", 0))
        precio_ejecutado = cummulative_quote_qty / executed_qty if executed_qty != 0 else 0
        # Registrar el trade en la base de datos
        registrar_trade("BTCUSDT", "BUY", executed_qty, precio_ejecutado, stop_loss, take_profit)
    except Exception as e:
        logger.error(f"Error al ejecutar orden de compra: {e}")
        enviar_mensaje_telegram(f"Error en orden de compra: {e}")

def ejecutar_orden_venta(stop_loss, take_profit):
    try:
        logger.info("Ejecutando orden de VENTA en BTC...")
        if SIMULAR:
            mensaje = (f"Simulación: Vender BTC | "
                       f"SL: {stop_loss:.2f}, TP: {take_profit:.2f}")
            logger.info(mensaje)
            enviar_mensaje_telegram(mensaje)
            registrar_trade("BTCUSDT", "SELL", CANTIDAD, 0, stop_loss, take_profit, status="SIMULATED")
            return
        # Obtener balance y verificar que haya BTC disponible
        balance = client.get_asset_balance(asset="BTC")
        cantidad_btc = float(balance.get("free", 0))
        if cantidad_btc <= 0:
            mensaje = "No hay BTC suficiente para vender"
            logger.info(mensaje)
            enviar_mensaje_telegram(mensaje)
            return
        # Ejecutar orden de venta de mercado
        order = client.order_market_sell(symbol="BTCUSDT", quantity=cantidad_btc)
        mensaje = f"Orden de venta ejecutada: {order}"
        logger.info(mensaje)
        enviar_mensaje_telegram(mensaje)
        # Configurar orden OCO para SL y TP (para cerrar la operación)
        oco_order = client.create_oco_order(
            symbol="BTCUSDT",
            side=Client.SIDE_BUY,
            quantity=cantidad_btc,
            price=str(take_profit),
            stopPrice=str(stop_loss),
            stopLimitPrice=str(stop_loss * 1.01),
            stopLimitTimeInForce="GTC"
        )
        mensaje_oco = f"OCO SL/TP ejecutada: {oco_order}"
        logger.info(mensaje_oco)
        enviar_mensaje_telegram(mensaje_oco)
        # Calcular precio promedio de venta
        executed_qty = float(order.get("executedQty", 0))
        cummulative_quote_qty = float(order.get("cummulativeQuoteQty", 0))
        precio_ejecutado = cummulative_quote_qty / executed_qty if executed_qty != 0 else 0
        # Registrar el trade en la base de datos
        registrar_trade("BTCUSDT", "SELL", executed_qty, precio_ejecutado, stop_loss, take_profit)
    except Exception as e:
        logger.error(f"Error al ejecutar orden de venta: {e}")
        enviar_mensaje_telegram(f"Error en orden de venta: {e}")

def ejecutar_trading():
    try:
        # Obtener la señal de la estrategia
        resultado = evaluar_mercado()
        accion = resultado.get("accion")
        if accion == "comprar":
            ejecutar_orden_compra(resultado.get("stop_loss"), resultado.get("take_profit"))
        elif accion == "vender":
            ejecutar_orden_venta(resultado.get("stop_loss"), resultado.get("take_profit"))
        else:
            logger.info("Mantener posición: sin operaciones.")
    except Exception as e:
        logger.error(f"Error en la ejecución del trading: {e}")
        enviar_mensaje_telegram(f"Error en la ejecución del trading: {e}")
