import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class REIScraper:
    def get_price(self, url):
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # REI suele usar clases claras
            title = soup.find('h1', id='product-page-title')
            title = title.get_text().strip() if title else "REI Product"
            
            # A veces es 'price-value' o 'current-price'
            price_span = soup.find('span', {'class': 'price-value'})
            if not price_span:
                price_span = soup.find('span', {'class': 'c-price__value'})

            price = 0.0
            if price_span:
                # Limpiar "$129.95" -> 129.95
                txt = price_span.get_text().strip().replace('$', '')
                price = float(txt)
            
            return price, title

        except Exception as e:
            print(f"Error scraping REI: {e}")
            return None, None