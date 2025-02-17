import streamlit as st
import pandas as pd

# ...
@st.cache_data
def carrega_dados(caminho):
    return pd.read_parquet(caminho)

dados = carrega_dados('../data/produtos.parquet')
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format='%d/%m/%Y')

st.title('Dados brutos')

# atributos selecionados da tabela
with st.expander('Atributos'):
    atributos = st.multiselect("Selecione as colunas", dados.columns.tolist(), dados.columns.tolist())

# função para criar filtros
def cria_filtro(df, coluna, tipo='multiselect', titulo=None, padrao=None):
    with st.sidebar.expander(coluna):
        if tipo == 'multiselect':
            return st.multiselect(titulo, df[coluna].unique().tolist(), default=padrao or df[coluna].unique().tolist())
        elif tipo == 'slider':
            return st.slider(titulo, int(df[coluna].min()), int(df[coluna].max()), padrao or (int(df[coluna].min()), int(df[coluna].max())))
        elif tipo == 'date_input':
            return st.date_input(titulo, padrao or (df[coluna].min(), df[coluna].max()))

# Criando os filtros
st.sidebar.title('Filtros')
produtos = cria_filtro(dados, 'Produto', titulo='Selecione os produtos')
categoria = cria_filtro(dados, 'Categoria do Produto', titulo='Selecione a categoria')
preco = cria_filtro(dados, 'Preço', tipo='slider', titulo='Selecione o preço', padrao=(0, 5000))
frete = cria_filtro(dados, 'Frete', tipo='slider', titulo='Selecione o frete')
data_compra = cria_filtro(dados, 'Data da Compra', tipo='date_input', titulo='Selecione a data')
vendedor = cria_filtro(dados, 'Vendedor', titulo='Selecione o vendedor')
local_compra = cria_filtro(dados, 'Local da compra', titulo='Selecione o local')
avaliacao_compra = cria_filtro(dados, 'Avaliação da compra', tipo='slider', titulo='Selecione a avaliação', padrao=(1, 5))
tipo_pagamento = cria_filtro(dados, 'Tipo de pagamento', titulo='Selecione o tipo de pagamento')
quantidade_parcelas = cria_filtro(dados, 'Quantidade de parcelas', tipo='slider', titulo='Selecione a quantidade de parcelas', padrao=(1, 12))

# dict para aplicar filtros em laço
filtros = {
    'Produto': produtos,
    'Categoria do Produto': categoria,
    'Preço': preco,
    'Frete': frete,
    'Data da Compra': data_compra,
    'Vendedor': vendedor,
    'Local da compra': local_compra,
    'Avaliação da compra': avaliacao_compra,
    'Tipo de pagamento': tipo_pagamento,
    'Quantidade de parcelas': quantidade_parcelas
}
# dict -> laco -> df
def aplica_filtros(df, filtros):
    for coluna, valor in filtros.items():
        if valor:
            if isinstance(valor, tuple):  # slider ou date_input
                if coluna == 'Data da Compra':
                    df = df[(df[coluna].dt.date >= valor[0]) & (df[coluna].dt.date <= valor[1])]
                else:
                    df = df[(df[coluna] >= valor[0]) & (df[coluna] <= valor[1])]
            else:  # multiselect
                df = df[df[coluna].isin(valor)]
    return df

dados_filtrados = aplica_filtros(dados, filtros)

# dados filtrados
st.dataframe(dados_filtrados[atributos])
st.markdown(f'Total de registros: :blue[{dados_filtrados.shape[0]}]')
st.markdown('---')

# dados filtrados em csv
st.download_button(
    label="Download CSV",
    data=dados_filtrados.to_csv(index=False).encode('utf-8'),
    file_name='dados.csv',
    mime='text/csv'
)