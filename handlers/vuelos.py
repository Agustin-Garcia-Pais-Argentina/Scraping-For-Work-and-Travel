from aiogram.types import Message
from scraping import flights
from scraping.flights import get_flight_price


async def handle_vuelos(message: Message):
    query = message.text.replace("/vuelos", "").strip()
    # soporta: jackson, idahofalls, driggs o por defecto jackson
    origin = 'JAC' # Jackson Hole
    if 'idaho' in query.lower():
        origin = 'IDA' # Idaho Falls (ejemplo)
    elif 'driggs' in query.lower():
        origin = 'JAC'


    # buscar JAC -> EZE (Buenos Aires EZE)
    flights = get_flight_price(origin, 'EZE')
    if not flights:
        await message.answer("No encontré vuelos ahora mismo.")
        return

    best = flights[0]
    text = (
    f"✈️ *Mejor opción {origin}->EZE*\n"
    f"Precio: ${best['price']}\n"
    f"Duración: {best['duration']}\n"
    f"Conexiones: {best['stops']}\n"
    f"Score estimado: {best.get('score', 'n/a')}\n"
    f"{best['url']}"
    )


    await message.answer(text, parse_mode='Markdown')