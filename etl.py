import requests
import pandas as pd


# EXTRACT   
try:
    url = 'https://labdados.com/produtos'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.HTTPError as err:
    print(f'Erro ao acessar o endpoint: {url} - {err}') if err.response is not None else print(err)

# TRANSFORM
df = pd.DataFrame(data)
df['Data da Compra'] = pd.to_datetime(df['Data da Compra'], format='%d/%m/%Y')

# LOAD
df.to_parquet('produtos.parquet', index=False)

