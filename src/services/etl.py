import requests
import pandas as pd
import logging
from typing import List, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extrai_dados(url:str) -> Optional[List[dict]]:
    """
        Extrai os dados da API e retorna uma lista de dicionários
    """
    logging.info(f'Acessando o endpoint: {url}')

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logging.info('Dados extraídos com sucesso')
        return response.json()
    
    except requests.exceptions.RequestException as err:
        logging.error(f'Erro ao acessar o endpoint: {url} - {err}')
        return None

def valida_dados(dados:dict) -> bool:
    """
        Função para validar os dados extraídos da API
    """
    if not isinstance(dados, list):
        logging.warning('Os dados extraídos da API nao sao uma lista')
        return False

    return True

def transforma_dados(data:dict) -> Optional[pd.DataFrame]:
    """
        Transforma os dados extraídos da API em um DataFrame
    """
    try:
        df = pd.DataFrame(data)
        logging.info('Dados transformados com sucesso')
        return df
    except Exception as err:
        logging.error(f'Erro ao transformar dados: {err}')
        return None

def carrega_dados(df:pd.DataFrame, caminho_arquivo:str) -> None:
    """
        Função para carregar os dados em um arquivo parquet
    """
    try:
        if not df.empty:
            df.to_parquet(caminho_arquivo, index=False)
            logging.info(f'Salvando os dados em {caminho_arquivo}')
        else:
            logging.warning('O DataFrame esta vazio')

    except Exception as err:
        logging.error(f'Erro ao salvar dados: {err}')

def executa_etl(url:str = 'https://labdados.com/produtos', caminho_arquivo:str = '../data/produtos.parquet') -> None:
    """
        Função principal para executar o ETL
    """

    dados = extrai_dados(url)
    
    if dados and valida_dados(dados):
        df = transforma_dados(dados)

        if df is not None:
            carrega_dados(df, caminho_arquivo)

if __name__ == '__main__':
    executa_etl()