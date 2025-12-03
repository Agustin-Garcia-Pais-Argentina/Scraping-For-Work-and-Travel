import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class AmazonScraper:
    def get_data(self, url):
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random,
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Intentar varios selectores de título
            title = soup.find(id='productTitle')
            title = title.get_text().strip() if title else "Producto Amazon"
            
            # Intentar varios selectores de precio (Amazon cambia esto seguido)
            price_element = soup.find('span', {'class': 'a-price-whole'})
            fraction_element = soup.find('span', {'class': 'a-price-fraction'})
            
            price = 0.0
            if price_element:
                price_text = price_element.get_text().replace('.', '').replace(',', '')
                price = float(price_text)
                if fraction_element:
                    price += float(fraction_element.get_text()) / 100
            
            return price, title
            
        except Exception as e:
            print(f"Error scraping Amazon: {e}")
            return None, None