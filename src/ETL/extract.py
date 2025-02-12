import logging
import requests
from transform import transforma_dados

logging.basicConfig(level=logging.ERROR)

def extrai_dados(url):
	"""
	Extrai dados de uma url e retorna conteudo em JSON

	: param url:  URL do endpoint
	: return: JSON | None
	"""
	try:
		response = requests.get(url, timeout=10)
		response.raise_for_status()
		dados = response.json()

		if not isinstance(dados, list):
			logging.error('Formato de dados inesperado')
			return None

		return response.json()
	
	except requests.exceptions.RequestException as err:
		print(f'Erro ao acessar o endpoint: {url} - {err}')
		return None


if __name__ == '__main__':
   url = 'https://labdados.com/produtos'
   dados = extrai_dados(url)
	
   if dados:
        transforma_dados(dados)
        print('Dados extraídos com sucesso')
   else:
	    print('Nenhum dado retornado')
