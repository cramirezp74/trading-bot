# 🚀 Bot de Trading Automático con Binance

Este bot de trading automatiza la compra y venta de Bitcoin en Binance utilizando una estrategia combinada basada en **RSI (Índice de Fuerza Relativa), EMA (Media Móvil Exponencial) y Bandas de Bollinger**. Puede operar en modo real o simulado y envía notificaciones a Telegram.

---

## 📌 Características

✅ **Obtención de datos** en tiempo real desde Binance.  
✅ **Estrategia combinada** con RSI, EMA y Bandas de Bollinger.  
✅ **Operaciones automáticas** de compra y venta de BTC/USDT.  
✅ **Modo de simulación** sin realizar transacciones reales.  
✅ **Registro de logs** detallado sobre las operaciones y el estado del mercado.  
✅ **Notificaciones en Telegram** sobre cada operación realizada.  

---

## 📦 Instalación

### 1️⃣ Clonar el repositorio
```sh
git clone https://github.com/tu_usuario/bot-trading.git
cd bot-trading
```

### 2️⃣ Crear un entorno virtual (opcional pero recomendado)
```sh
python -m venv venv
source venv/bin/activate  # En Linux/macOS
venv\Scripts\activate  # En Windows
```

### 3️⃣ Instalar dependencias
```sh
pip install -r requirements.txt
```

### 4️⃣ Configurar variables de entorno
Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
```ini
API_KEY=tu_api_key_de_binance
API_SECRET=tu_api_secret_de_binance
TELEGRAM_BOT_TOKEN=tu_token_de_telegram
TELEGRAM_CHAT_ID=tu_chat_id_de_telegram
CANTIDAD=50  # Monto en USDT por operación
INTERVALO=1h  # Intervalo de trading
RSI_SOBREVENTA=30
RSI_SOBRECOMPRA=70
SIMULAR=True  # Cambia a False para operar en modo real
```

---

## 🚀 Uso

Para ejecutar el bot, simplemente corre el siguiente comando:
```sh
python main.py
```
El bot analizará el mercado y tomará decisiones cada 60 minutos. Puedes modificar este intervalo en `config/settings.py`.

---

## 🛠 Estructura del Proyecto

```
bot-trading/
│── core/
│   ├── data_fetcher.py   # Obtiene datos de Binance
│   ├── trading.py        # Lógica de compra y venta
│── strategies/
│   ├── combined_strategy.py # Estrategia RSI + EMA + Bollinger
│── config/
│   ├── settings.py       # Configuración general
│   ├── logger.py         # Manejo de logs
│── utils/
│   ├── notifier.py       # Notificaciones de Telegram
│── main.py               # Archivo principal para ejecutar el bot
│── requirements.txt      # Dependencias necesarias
│── README.md             # Este archivo
│── .env                  # Variables de entorno (ignorado por git)
```

---

## ⚠️ Advertencias
- Este bot **NO garantiza ganancias**. Úsalo bajo tu propio riesgo.
- **Prueba en modo SIMULADO** antes de activar las transacciones reales.
- Asegúrate de contar con **fondos suficientes** en tu cuenta de Binance si operas en modo real.

---

## 📄 Licencia
Este proyecto se distribuye bajo la licencia MIT. Puedes modificarlo y usarlo libremente.

---

## 📩 Contacto
Si tienes dudas o sugerencias, contáctame en Telegram o GitHub.

