# etl.py
import requests
import pandas as pd

def extrai_dados(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f'Erro ao acessar o endpoint: {url} - {err}')
        return None

def transforma_dados(data):
    try:
        df = pd.DataFrame(data)
        return df
    except Exception as err:
        print(f'Erro ao transformar dados: {err}')
        return None

def carrega_dados(df, caminho_arquivo):
    try:
        df.to_parquet(caminho_arquivo, index=False)
        print(f'Dados salvos em {caminho_arquivo}')
    except Exception as err:
        print(f'Erro ao salvar dados: {err}')

def executa_etl():
    url = 'https://labdados.com/produtos'
    caminho_arquivo = '../data/produtos.parquet'

    dados = extrai_dados(url)
    if dados is not None:
        df = transforma_dados(dados)
        if df is not None:
            carrega_dados(df, caminho_arquivo)

if __name__ == '__main__':
    executa_etl()