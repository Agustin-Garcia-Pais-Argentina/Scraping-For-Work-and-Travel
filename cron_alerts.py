import asyncio
import os
from telegram import Bot
from db.db import Database
from scraping.amazon import AmazonScraper
from utils.scoring import calculate_score

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def run_cron():
    if not TOKEN:
        print("❌ No token")
        return

    print("📱 Iniciando Rastreo de Celulares...")
    bot = Bot(token=TOKEN)
    db = Database()
    products = db.get_products()
    
    scraper = AmazonScraper()

    for p in products:
        print(f"🔎 Check: {p['title'][:30]}...")
        
        # Como simplificamos, asumimos que todo es Amazon por ahora
        current_price, _ = scraper.get_data(p['url'])
        
        if current_price:
            # Guardamos precio para historial
            db.add_price(p['id'], current_price)
            
            # Calculamos si está "barato" históricamente
            history = db.get_price_history(p['id'])
            score = calculate_score(current_price, history, category='tech')
            
            # ALERTA: Si el precio es menor al target
            if current_price <= p['target_price']:
                diff = p['target_price'] - current_price
                msg = (
                    f"🚨 **OFERTA DETECTADA** 🚨\n\n"
                    f"📱 {p['title']}\n"
                    f"📉 **${current_price}** (Ahorrás ${diff:.2f})\n"
                    f"🎯 Objetivo: ${p['target_price']}\n"
                    f"🧠 Score: {score}/100\n\n"
                    f"🔗 [COMPRAR YA]({p['url']})"
                )
                try:
                    await bot.send_message(chat_id=p['chat_id'], text=msg, parse_mode='Markdown')
                    print(f"   ✅ Alerta enviada para {p['title']}")
                except Exception as e:
                    print(f"   ❌ Error enviando: {e}")
        else:
            print("   ⚠️ Error scrapeando precio.")

if __name__ == "__main__":
    asyncio.run(run_cron())