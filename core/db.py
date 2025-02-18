# core/db.py
import json
import mysql.connector
from mysql.connector import Error
from config.settings import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

def get_db_connection():
    """Obtiene y retorna una conexión a la base de datos MariaDB."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error al conectar a la base de datos MYSQL: {e}")
    return None

def registrar_trade(symbol, action, quantity, price, stop_loss, take_profit, status='OPEN'):
    """
    Registra una operación (trade) en la tabla 'trades'.
    
    Parámetros:
      - symbol: par de trading, por ejemplo "BTCUSDT"
      - action: "BUY" o "SELL"
      - quantity: cantidad ejecutada
      - price: precio promedio de ejecución
      - stop_loss, take_profit: niveles definidos
      - status: puede ser "OPEN", "CLOSED", "CANCELLED", "SIMULATED"
    """
    connection = get_db_connection()
    if connection is None:
        print("No se pudo conectar a la base de datos MYSQL.")
        return
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO trades (symbol, action, quantity, price, stop_loss, take_profit, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (symbol, action, quantity, price, stop_loss, take_profit, status))
        connection.commit()
        print("Trade registrado en la base de datos MYSQL.")
    except Error as e:
        print(f"Error al registrar el trade: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def registrar_market_data(symbol, open_time, close_time, open_val, high, low, close, volume):
    """
    Registra un registro de datos de mercado en la tabla 'market_data'.
    
    Parámetros:
      - symbol: Par de trading (por ejemplo, "BTCUSDT")
      - open_time: Fecha y hora de apertura (DATETIME)
      - close_time: Fecha y hora de cierre (DATETIME)
      - open_val, high, low, close: Valores numéricos correspondientes
      - volume: Volumen negociado
    """
    connection = get_db_connection()  # Usamos la función ya definida para obtener conexión
    if connection is None:
        print("No se pudo conectar a la base de datos MYSQL.")
        return
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO market_data (symbol, open_time, close_time, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (symbol, open_time, close_time, open_val, high, low, close, volume))
        connection.commit()
        print("Datos de mercado registrados en la base de datos MYSQL.")
    except Error as e:
        print(f"Error al registrar datos de mercado: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



def registrar_signal(symbol, signal, stop_loss, take_profit, motivos):
    """
    Registra la evaluación de la estrategia en la tabla 'strategy_signals'.
    
    Parámetros:
      - symbol: Par de trading (ej. "BTCUSDT")
      - signal: Señal generada ("comprar", "vender", "mantener")
      - stop_loss, take_profit: Niveles (o None si no aplican)
      - motivos: Detalle de las condiciones no cumplidas (puede ser un diccionario o cadena)
    """
    connection = get_db_connection()
    if connection is None:
        print("No se pudo conectar a la base de datos MariaDB.")
        return
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO strategy_signals (symbol, trade_signal, stop_loss, take_profit, motivos)
            VALUES (%s, %s, %s, %s, %s)
        """
        # Convertir 'motivos' a cadena JSON si es un diccionario o lista
        if motivos is not None and not isinstance(motivos, str):
            motivos_str = json.dumps(motivos)
        else:
            motivos_str = motivos
        cursor.execute(query, (symbol, signal, stop_loss, take_profit, motivos_str))
        connection.commit()
        print("Estrategia registrada en la base de datos.")
    except Error as e:
        print(f"Error al registrar la estrategia: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



def registrar_indicator_log(symbol, rsi, precio, ema5, ema9, macd, adx, atr, bb_lower, bb_upper):
    """
    Registra los valores de los indicadores en la tabla indicator_logs.
    
    Parámetros:
      - symbol: Par de trading (ej. "BTCUSDT")
      - rsi, precio, ema5, ema9, macd, adx, atr, bb_lower, bb_upper: Valores numéricos de los indicadores.
    """
    connection = get_db_connection()
    if connection is None:
        print("No se pudo conectar a la base de datos.")
        return
    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO indicator_logs (symbol, rsi, precio, ema5, ema9, macd, adx, atr, bb_lower, bb_upper)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (symbol, rsi, precio, ema5, ema9, macd, adx, atr, bb_lower, bb_upper))
        connection.commit()
        print("Log de indicadores registrado en la base de datos.")
    except Error as e:
        print(f"Error al registrar el log de indicadores: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()