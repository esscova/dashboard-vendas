import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# carregando os dados
# url = 'https://labdados.com/produtos'
# response = requests.get(url)
# dados = pd.DataFrame.from_dict(response.json())
dados = pd.read_parquet('produtos.parquet')

# util
def formata_numero(valor, prefixo = ''):
    for unidade in ['', 'mil']:
        if valor < 1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} milhoes'
# tratamento de dados
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format='%d/%m/%Y')

# calculos
receita = formata_numero(dados['Preço'].sum())
quantidade_de_vendas = formata_numero(dados.shape[0])

# tabelas
receita_dos_estados = dados.groupby('Local da compra')[['Preço']].sum()
receita_dos_estados = dados.drop_duplicates(subset=['Local da compra'])[['Local da compra', 'lat', 'lon']].merge(receita_dos_estados, how='left', left_on='Local da compra', right_index=True).sort_values(by='Preço', ascending=False)

receita_mensal = dados.set_index('Data da Compra').groupby(pd.Grouper(freq='ME'))[['Preço']].sum().reset_index()
receita_mensal['Ano'] = receita_mensal['Data da Compra'].dt.year
receita_mensal['Mes'] = receita_mensal['Data da Compra'].dt.month_name(locale='pt_BR')

receita_categorias = dados.groupby('Categoria do Produto')[['Preço']].sum().sort_values(by='Preço', ascending=False)

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
fig_receita_mensal = px.line(
    receita_mensal,
    x = 'Mes',
    y = 'Preço',
    markers=True,
    range_y=[0, receita_mensal['Preço'].max() * 1.1],
    color='Ano',
    line_dash='Ano',
    title='Receita mensal',
)
fig_receita_mensal.update_layout(
    yaxis_title='Receita',
)

fig_receita_estados = px.bar(
    receita_dos_estados.head(),
    x='Local da compra',
    y='Preço',
    title='Receita por estado',
    text_auto=True,
    template='plotly_white',
)
fig_receita_estados.update_layout(
    yaxis_title='Receita'
)
fig_receita_categorias = px.bar(
    receita_categorias,
    text_auto=True,
    title='Receita por categoria',
    template='plotly_white',
)
fig_receita_categorias.update_layout(
    yaxis_title='Receita'
)

# streamlit
st.set_page_config(
    layout="wide", 
    page_title='Dashboard de vendas', 
    page_icon=':bar_chart:'
)

st.title("DASHBOARD DE VENDAS :shopping_trolley:")

tab1, tab2, tab3 = st.tabs(["Receita", "Quantidade de vendas", "Vendedores"])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.metric('Receita', receita)
        st.plotly_chart(fig_mapa_receita, use_container_width=True)
        st.plotly_chart(fig_receita_estados, use_container_width=True)

    with col2:
        st.metric('Quantidade de vendas', quantidade_de_vendas)
        st.plotly_chart(fig_receita_mensal, use_container_width=True)
        st.plotly_chart(fig_receita_categorias, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.metric('Receita', receita)

    with col2:
        st.metric('Quantidade de vendas', quantidade_de_vendas)
with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.metric('Receita', receita)

    with col2:
        st.metric('Quantidade de vendas', quantidade_de_vendas)

# st.dataframe(dados)