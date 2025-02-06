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
receita_dos_estados = dados.groupby('Local da compra')[['Preço']].sum()
receita_dos_estados = dados.drop_duplicates(subset=['Local da compra'])[['Local da compra', 'lat', 'lon']].merge(receita_dos_estados, how='left', left_on='Local da compra', right_index=True).sort_values(by='Preço', ascending=False)
quantidade_de_vendas = formata_numero(dados.shape[0])

# graficos
fig_mapa_receita = px.scatter_geo(
    receita_dos_estados,
    lat='lat',
    lon='lon',
    scope='south america',
    size='Preço',
    hover_name='Local da compra',
    hover_data={'Preço': ':.2f', 'lat': False, 'lon': False},
    title='Receita por estado',
    color='Preço',
    projection='natural earth',
)

# streamlit
st.set_page_config(layout="wide")

st.title("DASHBOARD DE VENDAS :shopping_trolley:")
col1, col2 = st.columns(2)

with col1:
    st.metric('Receita', receita)
    st.plotly_chart(fig_mapa_receita, use_container_width=True)
    
with col2:
    st.metric('Quantidade de vendas', quantidade_de_vendas)

st.dataframe(dados)