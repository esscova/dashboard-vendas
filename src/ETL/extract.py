import requests

def extrai_dados(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as err:
        print(f'Erro ao acessar o endpoint: {url} - {err}')
        return None


if __name__ == '__main__':
    url = 'https://labdados.com/produtos'
    dados = extrai_dados(url)
    print(dados)