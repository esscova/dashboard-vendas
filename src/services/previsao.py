import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import joblib

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

def treina_modelo_vendas(df):
    """
    Função para treinar o modelo de previsão com base nos dados de vendas.
    Utiliza regressão linear para prever a receita de vendas com base no tempo.
    Retorna o modelo e as métricas de desempenho.
    """
    # features temporais
    df['Ano'] = df['Data da Compra'].dt.year
    df['Mes'] = df['Data da Compra'].dt.month
    df['Dia da Semana'] = df['Data da Compra'].dt.dayofweek  # 0 = segunda, 6 = domingo
    df['Trimestre'] = df['Data da Compra'].dt.quarter
    df['Dia do Mês'] = df['Data da Compra'].dt.day
    df['Fim de Semana'] = df['Data da Compra'].dt.dayofweek // 5  # 1 se for sábado ou domingo, 0 caso contrário

    X = df[['Ano', 'Mes', 'Dia da Semana', 'Trimestre', 'Dia do Mês', 'Fim de Semana']]
    y = df['Preço']
    
    # treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # escalonamento
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # treinamento
    modelo = LinearRegression()
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f'MSE: {mse:.2f}, MAE: {mae:.2f}, R²: {r2:.2f}')

    # modelo e o scaler
    joblib.dump(modelo, 'modelo.pkl')
    joblib.dump(scaler, 'scaler.pkl')

    return modelo, mse, mae, r2

def prever_vendas(ano, mes, dia_semana=None, trimestre=None, dia_mes=None, fim_de_semana=None):
    """
    Função para prever as vendas futuras.
    :param ano: ano da previsão
    :param mes: mês da previsão
    :param dia_semana: dia da semana (0 = segunda, 6 = domingo)
    :param trimestre: trimestre (1 a 4)
    :param dia_mes: dia do mês (1 a 31)
    :param fim_de_semana: 1 se for fim de semana, 0 caso contrário
    :return: previsão de receita
    """
    try:
        modelo = joblib.load('modelo.pkl')
        scaler = joblib.load('scaler.pkl')
    except Exception as e:
        raise ValueError(f"Erro ao carregar o modelo ou scaler: {e}")

    if dia_semana is None:
        dia_semana = pd.Timestamp(year=ano, month=mes, day=1).dayofweek
    if trimestre is None:
        trimestre = (mes - 1) // 3 + 1
    if dia_mes is None:
        dia_mes = 1  # Padrão: primeiro dia do mês
    if fim_de_semana is None:
        fim_de_semana = 1 if dia_semana >= 5 else 0

    X = np.array([[ano, mes, dia_semana, trimestre, dia_mes, fim_de_semana]])
    X_scaled = scaler.transform(X)
    previsao = modelo.predict(X_scaled)
    return previsao[0]

def grafico_previsao(df):
    """
    Gera o gráfico com as previsões de vendas para os próximos 5 anos.
    """
    # última data registrada nos dados
    ultimo_ano = df['Data da Compra'].dt.year.max()
    ultimo_mes = df['Data da Compra'].dt.month[df['Data da Compra'].dt.year == ultimo_ano].max()

    # prev
    previsao = []
    for ano in range(ultimo_ano, ultimo_ano + 6):  # De agora até 5 anos à frente
        for mes in range(1, 13):  # Para cada mês
            if ano == ultimo_ano and mes <= ultimo_mes:
                continue  # Pula meses que já passaram no último ano

            previsao.append([ano, mes, prever_vendas(ano, mes)])

    df_previsao = pd.DataFrame(previsao, columns=['Ano', 'Mes', 'Previsao'])

    df_previsao['Data'] = pd.to_datetime(df_previsao['Ano'].astype(str) + '-' + df_previsao['Mes'].astype(str) + '-01')

    fig = px.line(df_previsao, x='Data', y='Previsao', title='Previsão de Vendas Futuras (próximos 5 anos)')
    
    return fig