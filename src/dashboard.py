import streamlit as st
import pandas as pd
from utils import formata_numero, card_style
from data_processing import processa_dados, aplica_filtros
from plots import cria_graficos

#...
st.set_page_config(
    layout="wide",
    page_title='Dashboard de vendas',
    page_icon=':bar_chart:'
)
st.markdown(card_style, unsafe_allow_html=True)
#...
@st.cache_data
def carrega_dados(caminho):
    return pd.read_parquet(caminho)

dados = carrega_dados('../data/produtos.parquet')

# SIDEBAR

# titulo 
st.sidebar.title('Filtros')
regiao = st.sidebar.selectbox(
    'Selecione uma região',
    options=['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste', 'Brasil'], 
    index=5
)

# filtro anos
filtro_anos = st.sidebar.checkbox('Dados de todo o período', value=True)
if filtro_anos:
    ano = None
else:
    ano = st.sidebar.slider('Ano', 2020, 2023)
    
# filtro vendedores
filtro_vendedores = st.sidebar.multiselect(
    'Vendedores',
    dados['Vendedor'].unique()
)

# aplicando filtros
dados_filtrados = aplica_filtros(dados, regiao, ano, filtro_vendedores)
dados_processados = processa_dados(dados_filtrados)
graficos = cria_graficos(dados_processados)

# MAIN
st.title("DASHBOARD DE VENDAS :shopping_trolley:")
tab1, tab2, tab3 = st.tabs(["Receita", "Quantidade de vendas", "Vendedores"])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.metric('Receita', formata_numero(dados_processados['receita']))
        st.plotly_chart(graficos['fig_mapa_receita'], use_container_width=True)
        st.plotly_chart(graficos['fig_receita_estados'], use_container_width=True)

    with col2:
        st.metric('Quantidade de vendas', formata_numero(dados_processados['quantidade_de_vendas']))
        st.plotly_chart(graficos['fig_receita_mensal'], use_container_width=True)
        st.plotly_chart(graficos['fig_receita_categorias'], use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.metric('Quantidade de vendas', formata_numero(dados_processados['quantidade_de_vendas']))
        st.plotly_chart(graficos['fig_quantidade_vendas_estados'], use_container_width=True)
        # st.plotly_chart(graficos['fig_quantidade_vendas_mensal'], use_container_width=True)

    with col2:
        st.metric('Receita', formata_numero(dados_processados['receita']))
        st.plotly_chart(graficos['fig_quantidade_vendas_categorias'], use_container_width=True)

with tab3:
    input_top_vendedores = st.number_input('Top vendedores', 2, 10, 5)
    top_vendedores = dados_processados['receita_vendedores'].nlargest(input_top_vendedores, 'sum').reset_index()
    receita_top_vendedores = top_vendedores['sum'].sum()
    quantidade_vendas_top_vendedores = top_vendedores['count'].sum()
    graficos_vendedores = cria_graficos(dados_processados, input_top_vendedores=input_top_vendedores)

    col1, col2 = st.columns(2)

    with col1:
        st.metric('Receita (Top Vendedores)', formata_numero(receita_top_vendedores))
        st.plotly_chart(graficos_vendedores['fig_top_vendedores_receita'], use_container_width=True)

    with col2:
        st.metric('Quantidade de Vendas (Top Vendedores)', formata_numero(quantidade_vendas_top_vendedores))
        st.plotly_chart(graficos_vendedores['fig_top_vendedores_vendas'], use_container_width=True)