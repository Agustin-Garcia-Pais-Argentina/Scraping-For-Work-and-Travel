import asyncio
import os
from telegram import Bot
from db.db import Database
from scraping.amazon import AmazonScraper
from utils.scoring import calculate_score

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def run_cron():
    if not TOKEN:
        print("No token found")
        return

    print("⏰ Iniciando Cron Job...")
    bot = Bot(token=TOKEN)
    db = Database()
    products = db.get_products()
    
    scraper = AmazonScraper()

    for p in products:
        print(f"Checking: {p['title']}...")
        current_price = None
        
        # Router básico de scrapers
        if "amazon" in p['url']:
            current_price, _ = scraper.get_data(p['url'])
        
        if current_price:
            # Guardar historial
            db.add_price(p['id'], current_price)
            
            # Calcular score
            history = db.get_price_history(p['id'])
            score = calculate_score(current_price, history)
            
            # Verificar condiciones para alertar
            if current_price <= p['target_price']:
                message = (
                    f"🚨 **BAJÓ DE PRECIO!** 🚨\n\n"
                    f"📦 {p['title']}\n"
                    f"💵 Actual: **${current_price}**\n"
                    f"🎯 Objetivo: ${p['target_price']}\n"
                    f"🧠 Smart Score: {int(score)}/100\n\n"
                    f"🔗 [Comprar ahora]({p['url']})"
                )
                await bot.send_message(chat_id=p['chat_id'], text=message, parse_mode='Markdown')
            else:
                print(f"Precio ${current_price} no supera objetivo ${p['target_price']}")

if __name__ == "__main__":
    asyncio.run(run_cron())