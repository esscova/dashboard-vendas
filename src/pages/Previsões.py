import streamlit as st
import pandas as pd
from services.previsao import treina_modelo_vendas, prever_vendas, grafico_previsao
from services.data_processing import processa_dados

dados = pd.read_parquet('../data/produtos.parquet')
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format='%d/%m/%Y')
dados_processados = processa_dados(dados)

modelo, mse, mae, r2 = treina_modelo_vendas(dados)

st.title("Previsão de Vendas Futuras 📊")

tab1, tab2 = st.tabs(["Previsão de Vendas", "Desempenho do Modelo"])

with tab1:
    ano_inicial = 2024
    ano_final = 2028
    ano_selecionado = st.slider('Selecione o Ano para Previsão', min_value=ano_inicial, max_value=ano_final, value=2024)

    anos = []
    meses = []
    previsoes = []

    for mes in range(1, 13):
        dia_semana = pd.Timestamp(year=ano_selecionado, month=mes, day=1).dayofweek
        trimestre = (mes - 1) // 3 + 1
        previsao = prever_vendas(ano_selecionado, mes, dia_semana, trimestre)
        anos.append(ano_selecionado)
        meses.append(mes)
        previsoes.append(previsao)

    df_previsao = pd.DataFrame({
        'Ano': anos,
        'Mês': meses,
        'Previsão de Receita (R$)': previsoes
    })

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Previsões de Vendas para o Ano {ano_selecionado}")
        st.dataframe(df_previsao)

    with col2:
        grafico = grafico_previsao(dados)
        st.plotly_chart(grafico, use_container_width=True)

with tab2:
    st.subheader("Desempenho do Modelo")
    st.write(f"- **MSE (Erro Quadrático Médio):** {mse:.2f}")
    st.write(f"- **MAE (Erro Absoluto Médio):** {mae:.2f}")
    st.write(f"- **R² (Coeficiente de Determinação):** {r2}")