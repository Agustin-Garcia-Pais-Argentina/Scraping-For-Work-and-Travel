import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class AmazonScraper:
    def get_data(self, url):
        ua = UserAgent()
        # Headers rotativos y más completos para parecer un humano real
        headers = {
            'User-Agent': ua.random,
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'https://www.google.com/',
            'DNT': '1', # Do Not Track
            'Upgrade-Insecure-Requests': '1'
        }
        
        try:
            # Timeout un poco más largo por si Amazon tarda
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # --- 1. OBTENER TÍTULO ---
            title_elem = soup.find(id='productTitle')
            title = title_elem.get_text().strip() if title_elem else "Producto Amazon"
            
            # --- 2. OBTENER PRECIO (Lógica Mejorada) ---
            price = None

            # Estrategia A: Buscar el bloque "Precio a Pagar" (Usado en Ofertas)
            # Amazon suele poner el precio real dentro de un div con clase "priceToPay"
            price_to_pay = soup.find('div', {'class': 'priceToPay'})
            if price_to_pay:
                # Buscamos la parte entera dentro de ese bloque específico
                price_whole = price_to_pay.find('span', {'class': 'a-price-whole'})
                if price_whole:
                    # Limpiamos puntos y comas
                    txt = price_whole.get_text().replace('.', '').replace(',', '').strip()
                    price = float(txt)
                    
                    # Buscamos decimales (centavos)
                    price_fraction = price_to_pay.find('span', {'class': 'a-price-fraction'})
                    if price_fraction:
                        price += float(price_fraction.get_text()) / 100
                    
                    print(f"🎯 Detectada Oferta Especial: ${price}")

            # Estrategia B: Buscar selector clásico (Si no hubo oferta especial)
            if not price:
                price_element = soup.find('span', {'class': 'a-price-whole'})
                if price_element:
                    txt = price_element.get_text().replace('.', '').replace(',', '').strip()
                    price = float(txt)
                    
                    fraction_element = soup.find('span', {'class': 'a-price-fraction'})
                    if fraction_element:
                        price += float(fraction_element.get_text()) / 100

            # Estrategia C: Apex Price (A veces usado en deals viejos)
            if not price:
                apex_span = soup.find('span', {'class': 'apexPriceToPay'})
                if apex_span:
                    offscreen = apex_span.find('span', {'class': 'a-offscreen'})
                    if offscreen:
                        txt = offscreen.get_text().replace('$', '').replace(',', '').strip()
                        price = float(txt)

            if price:
                return price, title
            else:
                print("⚠️ No se encontró precio con ninguna estrategia.")
                return 0.0, title
            
        except Exception as e:
            print(f"❌ Error scraping Amazon: {e}")
            return None, None

# Test local rápido
if __name__ == "__main__":
    s = AmazonScraper()
    # Probá con el link de tu Pixel
    p, t = s.get_data("https://www.amazon.com/dp/B0CHX62V33") 
    print(f"Resultado Final: {t} -> ${p}")