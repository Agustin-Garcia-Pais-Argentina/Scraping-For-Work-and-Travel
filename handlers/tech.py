from telegram import Update
from telegram.ext import ContextTypes
from db.db import Database
from scraping.amazon import AmazonScraper # O BestBuy si lo agregás

async def tech_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("❌ Uso: /tech [URL] [TARGET]")
        return

    url = context.args[0]
    target = float(context.args[1])
    
    scraper = AmazonScraper()
    _, title = scraper.get_price(url) # Solo queremos validar que el link anda
    
    if title:
        db = Database()
        db.add_product(url, target, update.effective_chat.id, category='tech', title=title)
        await update.message.reply_text(f"💻 Tech Watch: {title}")
    else:
        await update.message.reply_text("⚠️ Link inválido.")