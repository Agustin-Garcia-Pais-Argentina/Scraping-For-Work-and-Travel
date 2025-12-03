import statistics

def analyze_history(price_list):
    """
    Recibe una lista de floats (precios históricos).
    Devuelve un diccionario con estadísticas clave.
    """
    if not price_list:
        return {
            "avg": 0, "min": 0, "max": 0, 
            "trend": "neutral", "volatility": 0
        }

    avg_price = statistics.mean(price_list)
    min_price = min(price_list)
    max_price = max(price_list)
    
    # Calcular tendencia (comparando el último tercio con el primero)
    # Si tenemos suficientes datos
    trend = "neutral"
    if len(price_list) >= 4:
        first_half = statistics.mean(price_list[:len(price_list)//2])
        last_half = statistics.mean(price_list[len(price_list)//2:])
        if last_half < first_half:
            trend = "baja"
        elif last_half > first_half:
            trend = "suba"

    return {
        "avg": round(avg_price, 2),
        "min": round(min_price, 2),
        "max": round(max_price, 2),
        "trend": trend,
        "count": len(price_list)
    }