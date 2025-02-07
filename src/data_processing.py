import pandas as pd

def processa_dados(df):
    # transformacoes
    df['Data da Compra'] = pd.to_datetime(df['Data da Compra'], format='%d/%m/%Y')

    # calculos
    receita = df['Preço'].sum()
    quantidade_de_vendas = df.shape[0]

    # tabelas
    receita_dos_estados = df.groupby('Local da compra')[['Preço']].sum()
    receita_dos_estados = df.drop_duplicates(subset=['Local da compra'])[['Local da compra', 'lat', 'lon']].merge(
        receita_dos_estados, how='left', left_on='Local da compra', right_index=True
    ).sort_values(by='Preço', ascending=False)

    receita_mensal = df.set_index('Data da Compra').groupby(pd.Grouper(freq='ME'))[['Preço']].sum().reset_index()
    receita_mensal['Ano'] = receita_mensal['Data da Compra'].dt.year
    receita_mensal['Mes'] = receita_mensal['Data da Compra'].dt.month_name(locale='pt_BR')

    receita_categorias = df.groupby('Categoria do Produto')[['Preço']].sum().sort_values(by='Preço', ascending=False)

    receita_vendedores = df.groupby('Vendedor')['Preço'].agg(['sum', 'count'])

    return {
        'receita': receita,
        'quantidade_de_vendas': quantidade_de_vendas,
        'receita_dos_estados': receita_dos_estados,
        'receita_mensal': receita_mensal,
        'receita_categorias': receita_categorias,
        'receita_vendedores': receita_vendedores
    }

def aplica_filtros(df, regiao, ano, vendedores):
    if regiao != 'Brasil':
        df = df[df['Local da compra'].str.contains(regiao, case=False)]

    if ano is not None:
        df = df[df['Data da Compra'].dt.year == ano]

    if vendedores:
        df = df[df['Vendedor'].isin(vendedores)]

    return df