import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class FlightScraper:
    def get_flight_price(self, origin, destination, date_str):
        """
        Busca el precio más barato en Google Flights para un tramo de IDA.
        date_str debe estar en formato YYYY-MM-DD.
        """
        # Configurar URL de Google Flights
        # Ejemplo: https://www.google.com/travel/flights?q=Flights%20to%20MIA%20from%20EZE%20on%202025-05-10
        url = f"https://www.google.com/travel/flights?q=Flights%20to%20{destination}%20from%20{origin}%20on%20{date_str}"
        
        print(f"✈️ Buscando vuelos: {origin} -> {destination} ({date_str})")
        
        # Configurar Chrome Headless (para servidores)
        chrome_options = Options()
        chrome_options.add_argument("--headless") # No abrir ventana
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        # User Agent para parecer un navegador real y no un bot
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

        driver = None
        try:
            # Inicializar Driver (instala ChromeDriver automáticamente)
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            driver.get(url)

            # Esperar hasta 10 segundos a que aparezca el elemento de precio
            # Google Flights suele usar la clase '.YMlIz' o 'span[role="text"]' para precios destacados
            # Nota: Estas clases (CSS Selectors) cambian a veces. 
            # Una estrategia robusta es buscar el símbolo de moneda.
            
            wait = WebDriverWait(driver, 15)
            
            # Intentamos buscar el primer precio visible en la lista de "Mejores vuelos"
            # El xpath busca cualquier elemento que contenga el signo $ y sea un número
            price_element = wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="YMlIz FpEdX"]//span'))
            )
            
            if not price_element:
                # Fallback: intentar otro selector común en Google Flights
                price_element = driver.find_element(By.XPATH, '(//span[@role="text" and contains(text(), "$")])[1]')

            price_text = price_element.text.strip()
            
            # Limpieza: "$950" -> 950.0
            # A veces viene como "US$950" o "$1,200"
            clean_price = price_text.replace('US', '').replace('$', '').replace(',', '').replace('.', '')
            
            # En Argentina a veces google muestra $1.000.000, hay que tener cuidado con el punto
            # Asumimos precio en USD si usás VPN o configuración US, sino ARS.
            # Para este bot asumimos que devuelve un entero.
            
            return float(clean_price), f"Vuelo Google {origin}-{destination}"

        except Exception as e:
            logging.error(f"Error scraping vuelos: {e}")
            return None, None
            
        finally:
            if driver:
                driver.quit()

# Para probarlo solo:
if __name__ == "__main__":
    scraper = FlightScraper()
    precio, titulo = scraper.get_flight_price("EZE", "MIA", "2024-12-25")
    print(f"Resultado: {titulo} - ${precio}")