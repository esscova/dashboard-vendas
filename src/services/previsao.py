import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

def treina_modelo_vendas(df):
    """
    Função para treinar o modelo de previsão com base nos dados de vendas.
    Utiliza regressão linear para prever a receita de vendas com base no tempo.
    Retorna o modelo e as métricas de desempenho
    """

    df['Ano'] = df['Data da Compra'].dt.year
    df['Mes'] = df['Data da Compra'].dt.month

    X = df[['Ano', 'Mes']]
    y = df['Preço']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    modelo = LinearRegression()
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f'MSE: {mse:.2f}, MAE: {mae:.2f}, R²: {r2:.2f}')

    return modelo, mse, mae, r2

def prever_vendas(modelo, ano, mes):
    """
    Função para prever as vendas futuras.
    :param modelo: modelo treinado
    :param ano: ano da previsão
    :param mes: mês da previsão
    :return: previsão de receita
    """
    X = np.array([[ano, mes]])
    previsao = modelo.predict(X)
    return previsao[0]


# services/previsao.py

def grafico_previsao(modelo, df):
    """
    Gera o gráfico com as previsões de vendas para os próximos 5 anos.
    """
    # Identificar a última data registrada nos dados
    ultimo_ano = df['Data da Compra'].dt.year.max()
    ultimo_mes = df['Data da Compra'].dt.month[df['Data da Compra'].dt.year == ultimo_ano].max()

    # Gerar previsões para os próximos 5 anos
    previsao = []
    for ano in range(ultimo_ano, ultimo_ano + 6):  # De agora até 5 anos à frente
        for mes in range(1, 13):  # Para cada mês
            if ano == ultimo_ano and mes <= ultimo_mes:
                continue  # Pula meses que já passaram no último ano

            previsao.append([ano, mes, prever_vendas(modelo, ano, mes)])

    # Criar DataFrame com as previsões
    df_previsao = pd.DataFrame(previsao, columns=['Ano', 'Mes', 'Previsao'])

    # Criar a coluna 'Data' no formato 'YYYY-MM-01' para o primeiro dia de cada mês
    df_previsao['Data'] = pd.to_datetime(df_previsao['Ano'].astype(str) + '-' + df_previsao['Mes'].astype(str) + '-01')

    # Criar o gráfico de linha
    fig = px.line(df_previsao, x='Data', y='Previsao', title='Previsão de Vendas Futuras (próximos 5 anos)')
    return fig
