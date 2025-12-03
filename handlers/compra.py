from telegram import Update
from telegram.ext import ContextTypes
from db.db import Database
from scraping.amazon import AmazonScraper

async def compra_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Uso: /compra [LINK] [TARGET_PRICE]
    if len(context.args) < 2:
        await update.message.reply_text("❌ Uso incorrecto. Ejemplo:\n/compra https://amazon.com/... 500")
        return

    url = context.args[0]
    try:
        target = float(context.args[1])
    except ValueError:
        await update.message.reply_text("❌ El precio debe ser un número.")
        return

    msg = await update.message.reply_text("🔍 Analizando link...")
    
    # Pre-check rápido para sacar el título
    scraper = AmazonScraper()
    price, title = scraper.get_data(url)
    
    if title:
        db = Database()
        db.add_product(url, target, update.effective_chat.id, title=title)
        await msg.edit_text(f"✅ **Guardado!**\n📦 {title}\n🎯 Te aviso si baja de ${target} USD")
    else:
        await msg.edit_text("⚠️ No pude leer el link. Asegurate que sea de Amazon o verifícalo.")