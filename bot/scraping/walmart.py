import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json

class WalmartScraper:
    def get_price(self, url):
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code != 200:
                print(f"Walmart Blocked/Error: {response.status_code}")
                return None, None

            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Walmart suele guardar info en un tag script JSON-LD
            script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
            if script_tag:
                data = json.loads(script_tag.string)
                # Navegar el JSON es complejo y cambia, fallback a HTML:
            
            # Selector HTML clásico (puede cambiar)
            price_span = soup.find('span', {'itemprop': 'price'})
            title_h1 = soup.find('h1')
            
            title = title_h1.get_text().strip() if title_h1 else "Walmart Item"
            price = 0.0
            
            if price_span:
                price_text = price_span.get_text().replace('$', '').replace(',', '')
                price = float(price_text)
                
            return price, title
            
        except Exception as e:
            print(f"Error scraping Walmart: {e}")
            return None, None