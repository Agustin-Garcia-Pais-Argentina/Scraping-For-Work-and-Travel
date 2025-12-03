import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from db.db import Database
from scraping.amazon import AmazonScraper

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def track_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Uso: /track [LINK_AMAZON] [PRECIO_MAXIMO]
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("❌ Uso: `/track https://amazon.com/... 500`", parse_mode='Markdown')
        return

    url = args[0]
    try:
        target = float(args[1])
    except ValueError:
        await update.message.reply_text("❌ El precio debe ser un número (ej: 500).")
        return

    msg = await update.message.reply_text("🔍 Analizando celular...")

    scraper = AmazonScraper()
    price, title = scraper.get_data(url)

    if title:
        db = Database()
        # Guardamos con categoría 'phone'
        db.add_product(url, target, update.effective_chat.id, category='phone', title=title)
        
        text = (
            f"📱 **Celular Rastreado**\n"
            f"📦 {title}\n"
            f"💵 Precio Actual: **${price}**\n"
            f"🎯 Te aviso si baja de: **${target}**"
        )
        await msg.edit_text(text, parse_mode='Markdown')
    else:
        await msg.edit_text("⚠️ No pude leer el link. Asegurate que sea de Amazon.")

if __name__ == '__main__':
    if not TOKEN:
        print("Error: Sin token")
        exit()
        
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Un solo comando poderoso
    app.add_handler(CommandHandler("track", track_handler))
    
    print("📱 Phone Tracker Bot iniciado...")
    app.run_polling()