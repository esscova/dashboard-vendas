import sqlite3
import logging

logging.basicConfig(level=logging.ERROR)

def transforma_dados(data):
    try:
        if not isinstance(data, list):
            logging.error('Formato de dados inesperado')
            return False
        
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto TEXT,
                categoria TEXT,
                preco REAL,
                frete REAL,
                data_compra TEXT,
                vendedor TEXT,
                local_compra TEXT,
                avaliacao INTEGER,
                tipo_pagamento TEXT,
                parcelas INTEGER,
                lat REAL,
                lon REAL
            )
            ''')
            required_fields = ['Produto', 'Categoria do Produto', 'Preço', 'Frete', 'Data da Compra', 'Vendedor', 'Local da compra', 'Avaliação da compra', 'Tipo de pagamento', 'Quantidade de parcelas', 'lat', 'lon']

            for item in data:
                if not all(field in item for field in required_fields):
                    logging.error(f'Campos faltantes no item: {item}')
                    continue
                cursor.execute('SELECT produto, data_compra FROM produtos WHERE produto = ? AND data_compra = ?', (item['Produto'], item['Data da Compra']))
                
                if cursor.fetchone():
                    logging.warning(f'Item já existe: {item["Produto"]} - {item["Data da Compra"]}')
                    continue

                cursor.execute('''
                INSERT INTO produtos (
                    produto, categoria, preco, frete, data_compra, vendedor, local_compra, avaliacao, tipo_pagamento, parcelas, lat, lon
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    item['Produto'],
                    item['Categoria do Produto'],
                    item['Preço'],
                    item['Frete'],
                    item['Data da Compra'],
                    item['Vendedor'],
                    item['Local da compra'],
                    item['Avaliação da compra'],
                    item['Tipo de pagamento'],
                    item['Quantidade de parcelas'],
                    item['lat'],
                    item['lon']
                ))
        conn.commit()
        conn.close()
        return f'{len(data)} registros processados com sucesso.'
        
    except Exception as e:
        print(f'Erro ao transformar dados: {e}')
        return False