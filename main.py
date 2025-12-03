import logging
from telegram.ext import ApplicationBuilder, CommandHandler
from handlers.compra import compra_handler
from handlers.celular import celular_handler
from handlers.ropa import ropa_handler
from handlers.tech import tech_handler
from handlers.vuelos import handle_vuelos as vuelos_handler
import os

# Configuración de Logs (útil para ver si falla algo en consola)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# TU TOKEN (Te recomiendo pasarlo a .env para prod, pero acá lo hardcodeamos para probar ya)
TOKEN = os.getenv("TELEGRAM_TOKEN")

if __name__ == '__main__':
    print("🚀 Iniciando Driggs Smart Buyer Bot...")
    
    # 1. Construir la aplicación
    app = ApplicationBuilder().token(TOKEN).build()
    
    # 2. Registrar los Comandos (Handlers)
    # Sintaxis: /comando -> función que lo maneja
    app.add_handler(CommandHandler("compra", compra_handler))   # Amazon general
    app.add_handler(CommandHandler("celular", celular_handler)) # Planes USA
    app.add_handler(CommandHandler("ropa", ropa_handler))       # REI / Invierno
    app.add_handler(CommandHandler("tech", tech_handler))       # Gadgets
    app.add_handler(CommandHandler("vuelos", vuelos_handler))   # Pasajes
    
    # 3. Correr el bot (Polling)
    print("🤖 Bot escuchando! Probá enviar /compra o /vuelos en Telegram.")
    app.run_polling()