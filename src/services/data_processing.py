import pandas as pd

def processa_dados(df):
    # transformacao
    df.loc[:,'Data da Compra'] = pd.to_datetime(df['Data da Compra'], format='%d/%m/%Y')

    # calculos
    receita = df['Preço'].sum()
    quantidade_de_vendas = df.shape[0]

    # tabelas
    receita_dos_estados = df.groupby('Local da compra')[['Preço']].sum()
    receita_dos_estados = df.drop_duplicates(subset=['Local da compra'])[['Local da compra', 'lat', 'lon']].merge(
        receita_dos_estados, how='left', left_on='Local da compra', right_index=True
    ).sort_values(by='Preço', ascending=False)

    quantidade_vendas_estados = df.groupby('Local da compra').size().reset_index(name='Quantidade de Vendas')

    receita_mensal = df.set_index('Data da Compra').groupby(pd.Grouper(freq='ME'))[['Preço']].sum().reset_index()
    receita_mensal['Ano'] = receita_mensal['Data da Compra'].dt.year
    receita_mensal['Mes'] = receita_mensal['Data da Compra'].dt.month

    meses_pt = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
        5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
        9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }
    receita_mensal['Mes'] = receita_mensal['Mes'].map(meses_pt)

    quantidade_vendas_mensal = df.set_index('Data da Compra').groupby(pd.Grouper(freq='ME')).size().reset_index(name='Quantidade de Vendas')
    quantidade_vendas_mensal['Ano'] = quantidade_vendas_mensal['Data da Compra'].dt.year
    quantidade_vendas_mensal['Mes'] = quantidade_vendas_mensal['Data da Compra'].dt.month
    quantidade_vendas_mensal['Mes'] = quantidade_vendas_mensal['Mes'].map(meses_pt)

    receita_categorias = df.groupby('Categoria do Produto')[['Preço']].sum().sort_values(by='Preço', ascending=False)
    quantidade_vendas_categorias = df.groupby('Categoria do Produto').size().reset_index(name='Quantidade de Vendas')

    receita_vendedores = df.groupby('Vendedor')['Preço'].agg(['sum', 'count'])

    return {
        'receita': receita,
        'quantidade_de_vendas': quantidade_de_vendas,
        'receita_dos_estados': receita_dos_estados,
        'quantidade_vendas_estados': quantidade_vendas_estados,
        'receita_mensal': receita_mensal,
        'quantidade_vendas_mensal': quantidade_vendas_mensal,
        'receita_categorias': receita_categorias,
        'quantidade_vendas_categorias': quantidade_vendas_categorias,
        'receita_vendedores': receita_vendedores
    }

def aplica_filtros(df, regiao, ano, vendedores):
    estados_para_regioes = {
        'Norte': ['AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO'],
        'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
        'Sudeste': ['ES', 'MG', 'RJ', 'SP'],
        'Sul': ['PR', 'RS', 'SC'],
        'Centro-Oeste': ['DF', 'GO', 'MS', 'MT']
    }
    
    if regiao != 'Brasil':
        estados = estados_para_regioes.get(regiao, [])
        df = df.loc[df['Local da compra'].isin(estados)]

    if ano is not None:
        df = df.loc[df['Data da Compra'].dt.year == ano]

    if vendedores:
        df = df.loc[df['Vendedor'].isin(vendedores)]

    return df
