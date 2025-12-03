from utils.price_history import analyze_history

def calculate_score(current_price, price_history, category='general'):
    """
    Retorna Score 0-100.
    """
    stats = analyze_history(price_history)
    
    # 1. Si no hay historia, el score es neutro tirando a bajo (riesgo)
    if stats["count"] == 0:
        return 50

    score = 50.0

    # 2. Factor Precio vs Promedio Histórico (Peso: 40%)
    # Si precio actual es 20% menos que el promedio -> Suma 20 pts
    diff_perc = ((stats["avg"] - current_price) / stats["avg"]) * 100
    score += diff_perc * 1.5  # Multiplicador de impacto

    # 3. Factor Mínimo Histórico (Peso: 30%)
    # Si rompe el récord histórico de barato -> Bonus grande
    if current_price <= stats["min"]:
        score += 25
    elif current_price <= stats["min"] * 1.05: # Cerca del minimo (5%)
        score += 10

    # 4. Ajustes por Categoría
    if category == 'tech':
        # Tech se devalúa rápido, exigimos descuentos más agresivos
        score -= 5 
    elif category == 'ropa':
        # Ropa tiene márgenes altos, los descuentos suelen ser reales
        pass

    # Cap a 0-100
    return max(0, min(100, int(score)))