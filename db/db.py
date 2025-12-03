import sqlite3
import os
import sys

class Database:
    def __init__(self, db_name="prices.db"):
        # Calculamos la ruta absoluta al directorio actual (db/)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, db_name)
        
        # Conectamos (esto crea el archivo vacío si no existe)
        self.conn = sqlite3.connect(self.db_path)
        
        # Intentamos crear las tablas
        self.create_tables()

    def create_tables(self):
        # Buscamos el schema en la misma carpeta que este script
        schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schema.sql')
        
        print(f"📂 DEBUG: Buscando schema en: {schema_path}")
        
        if not os.path.exists(schema_path):
            print("❌ ERROR CRÍTICO: El archivo schema.sql NO EXISTE en la ruta especificada.")
            print("📁 Archivos encontrados en esa carpeta:")
            print(os.listdir(os.path.dirname(schema_path)))
            # Forzamos un error para que GitHub Actions se ponga rojo y veamos esto
            sys.exit(1) 
            
        try:
            with open(schema_path, 'r') as f:
                self.conn.executescript(f.read())
            self.conn.commit()
            print("✅ Tablas creadas/verificadas correctamente.")
        except Exception as e:
            print(f"❌ Error ejecutando SQL: {e}")

    def add_product(self, url, target_price, chat_id, category='general', title=None):
        self.conn.execute(
            "INSERT INTO products (url, target_price, chat_id, category, title) VALUES (?, ?, ?, ?, ?)",
            (url, target_price, chat_id, category, title)
        )
        self.conn.commit()

    def get_products(self):
        # Esta es la línea que fallaba antes
        try:
            cursor = self.conn.execute("SELECT id, url, target_price, chat_id, title, category FROM products")
            columns = [column[0] for column in cursor.description]
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results
        except sqlite3.OperationalError as e:
            print(f"❌ Error leyendo productos: {e}")
            # Si falla aquí, es porque la tabla no se creó arriba
            return []

    def add_price(self, product_id, price):
        self.conn.execute(
            "INSERT INTO price_history (product_id, price) VALUES (?, ?)",
            (product_id, price)
        )
        self.conn.commit()

    def get_price_history(self, product_id):
        cursor = self.conn.execute(
            "SELECT price FROM price_history WHERE product_id = ? ORDER BY scraped_at DESC LIMIT 30",
            (product_id,)
        )
        return [row[0] for row in cursor.fetchall()]