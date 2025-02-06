import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# carregando os dados
url = 'https://labdados.com/produtos'
response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json())

# util
def formata_numero(valor, prefixo = ''):
    for unidade in ['', 'mil']:
        if valor < 1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} milhoes'

# calculos
receita = formata_numero(dados['Preço'].sum())
quantidade_de_vendas = formata_numero(dados.shape[0])

# graficos


# streamlit
st.set_page_config(layout="wide")

st.title("DASHBOARD DE VENDAS :shopping_trolley:")
col1, col2 = st.columns(2)

with col1:
    st.metric('Receita', receita)
with col2:
    st.metric('Quantidade de vendas', quantidade_de_vendas)

st.dataframe(dados)