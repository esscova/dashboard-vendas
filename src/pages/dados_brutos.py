import streamlit as st
import pandas as pd


# ...

@st.cache_data
def carrega_dados(caminho):
    return pd.read_parquet(caminho)

dados = carrega_dados('../data/produtos.parquet')
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format='%d/%m/%Y')

st.title('Dados brutos')

with st.expander('Atributos'):
    atributos = st.multiselect("Selecione os atributos", dados.columns.tolist(), dados.columns.tolist())

st.sidebar.title('Filtros')
with st.sidebar.expander('Produto'):
    produtos = st.multiselect("Selecione os produtos", dados['Produto'].unique().tolist(), dados['Produto'].unique().tolist())

with st.sidebar.expander('Categoria do Produto'):
    categoria = st.multiselect('Selecione a categoria', dados['Categoria do Produto'].unique().tolist(), dados['Categoria do Produto'].unique().tolist())

with st.sidebar.expander('Preço'):   
    preco = st.slider('Selecione o preço', 0, 5000, (0, 5000))

with st.sidebar.expander('Frete'):
    frete = st.slider('Selecione o frete', 0, int(dados['Frete'].max()), (0, int(dados['Frete'].max())))

with st.sidebar.expander('Data da compra'):
    data_compra = st.date_input('Selecione a data', ((dados['Data da Compra'].min(), dados['Data da Compra'].max())))

with st.sidebar.expander('Vendedor'):
    vendedor = st.multiselect('Selecione o vendedor', dados['Vendedor'].unique().tolist(), dados['Vendedor'].unique().tolist())

with st.sidebar.expander('Local da compra'):
    local_compra = st.multiselect('Selecione o local', dados['Local da compra'].unique().tolist(), dados['Local da compra'].unique().tolist())

with st.sidebar.expander('Avaliação da compra'):
    avaliacao_compra = st.slider('Selecione a avaliação', 1, 5, (1, 5))

with st.sidebar.expander('Tipo de pagamento'):
    tipo_pagamento = st.multiselect('Selecione o tipo de pagamento', dados['Tipo de pagamento'].unique().tolist(), dados['Tipo de pagamento'].unique().tolist())

with st.sidebar.expander('Quantidade de parcelas'):
    quantidade_parcelas = st.slider('Selecione a quantidade de parcelas', 1, 12, (1, 12))

st.dataframe(dados)