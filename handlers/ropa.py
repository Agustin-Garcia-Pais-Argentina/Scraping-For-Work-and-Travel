from telegram import Update
from telegram.ext import ContextTypes
from db.db import Database
from scraping.rei import REIScraper

async def ropa_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Uso: /ropa [URL_REI] [TARGET]
    if len(context.args) < 2:
        await update.message.reply_text("❌ Uso: /ropa [URL_REI] [PRECIO_MAX]")
        return

    url = context.args[0]
    target = float(context.args[1])
    
    scraper = REIScraper()
    price, title = scraper.get_price(url)
    
    if title:
        db = Database()
        db.add_product(url, target, update.effective_chat.id, category='ropa', title=title)
        await update.message.reply_text(f"🧥 Guardado: {title}\nPrecio actual: ${price}")
    else:
        await update.message.reply_text("⚠️ No pude leer el link de REI.")