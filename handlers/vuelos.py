from aiogram.types import Message
from scraping.flights import FlightScraper
import datetime
import random




async def handle_vuelos(message: Message):
    query = message.text.replace("/vuelos", "").strip()
    # soporta: jackson, idahofalls, driggs o por defecto jackson
    origin = 'JAC' # Jackson Hole
    if 'idaho' in query.lower():
        origin = 'IDA' # Idaho Falls (ejemplo)
    elif 'driggs' in query.lower():
        origin = 'JAC'

    start = datetime.date(2026, 3, 15)
    end = datetime.date(2026, 3, 30)
    delta_days = (end - start).days
    scraper = FlightScraper()
    chosen_date = start + datetime.timedelta(days=random.randint(0, delta_days))
    date_str = chosen_date.strftime("%Y-%m-%d")
    
    scraper = FlightScraper()
    price, best = scraper.get_flight_price(origin, 'EZE', date_str)
    
    
    if not price:
        await message.answer("No encontré vuelos ahora mismo.")
        return

    text = (
    f"✈️ *Mejor opción {origin}->EZE*\n"
    f"Precio: ${best['price']}\n"
    f"Duración: {best['duration']}\n"
    f"Conexiones: {best['stops']}\n"
    f"Score estimado: {best.get('score', 'n/a')}\n"
    f"{best['url']}"
    )


    await message.answer(text, parse_mode='Markdown')