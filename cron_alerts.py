import asyncio
import os
from telegram import Bot
from db.db import Database
from scraping.amazon import AmazonScraper
from utils.scoring import calculate_score
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TOKEN = os.getenv("TELEGRAM_TOKEN")
# IMPORTANTE: Leemos también tu ID para poder crear el producto a tu nombre
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def run_cron():
    if not TOKEN:
        print("❌ Error: No token found")
        return

    print("⏰ Iniciando Cron Job...")
    bot = Bot(token=TOKEN)
    db = Database()
    products = db.get_products()
    scraper = AmazonScraper()

    for p in products:
        print(f"🔎 Analizando: {p['title']}...")
        current_price = None
        
        # Router básico
        if "amazon" in p['url']:
            current_price, _ = scraper.get_data(p['url'])
        
        if current_price:
            print(f"   💲 Precio encontrado: ${current_price}")
            db.add_price(p['id'], current_price)
            
            history = db.get_price_history(p['id'])
            score = calculate_score(current_price, history)
            
            # Como pusimos target $99,999, esto SIEMPRE va a ser verdadero
            if current_price <= p['target_price']:
                print("   🚨 ¡CONDICIÓN CUMPLIDA! Enviando mensaje...")
                message = (
                    f"🚨 **ALERTA DE PRUEBA** 🚨\n\n"
                    f"📦 {p['title']}\n"
                    f"💵 Actual: **${current_price}**\n"
                    f"🎯 Objetivo: ${p['target_price']}\n"
                    f"🧠 Smart Score: {int(score)}/100\n\n"
                    f"🔗 [Ver en Amazon]({p['url']})"
                )
                try:
                    await bot.send_message(chat_id=p['chat_id'], text=message, parse_mode='Markdown')
                    print("   ✅ Mensaje enviado a Telegram.")
                except Exception as e:
                    print(f"   ❌ Error enviando a Telegram: {e}")
            else:
                print(f"   📉 Precio ${current_price} no supera objetivo")
        else:
            print("   ⚠️ No se pudo obtener el precio.")

if __name__ == "__main__":
    asyncio.run(run_cron())