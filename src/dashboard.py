import streamlit as st
import pandas as pd
from utils import formata_numero
from data_processing import processa_dados
from plots import cria_graficos

#...

dados = pd.read_parquet('../data/produtos.parquet')
dados_processados = processa_dados(dados)
graficos = cria_graficos(dados_processados)

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
        st.metric('Receita', formata_numero(dados_processados['receita']))

    with col2:
        st.metric('Quantidade de vendas', formata_numero(dados_processados['quantidade_de_vendas']))

with tab3:
    input_top_vendedores = st.number_input('Top vendedores',2,10,5)
    graficos = cria_graficos(dados_processados, input=input_top_vendedores)

    col1, col2 = st.columns(2)

    with col1:
        st.metric('Receita', formata_numero(dados_processados['receita']))
        st.plotly_chart(graficos['fig_receita_vendedores'], use_container_width=True)
    with col2:
        st.metric('Quantidade de vendas', formata_numero(dados_processados['quantidade_de_vendas']))

    