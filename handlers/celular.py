from telegram import Update
from telegram.ext import ContextTypes
from db.db import Database

async def celular_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Uso: /celular verizon start 60
    args = context.args
    if len(args) < 3:
        await update.message.reply_text("❌ Uso: /celular [CARRIER] [PLAN] [TARGET_PRICE]")
        return

    carrier = args[0]
    plan = args[1]
    target = float(args[2])
    
    # Generamos una 'URL' ficticia interna para trackearlo
    pseudo_url = f"plan://{carrier}/{plan}"
    
    db = Database()
    db.add_product(pseudo_url, target, update.effective_chat.id, category='celular', title=f"Plan {carrier} {plan}")
    
    await update.message.reply_text(f"📱 Monitoreando plan {carrier} {plan} por menos de ${target}")