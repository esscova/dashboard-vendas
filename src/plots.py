import plotly.express as px
def cria_graficos(dados_processados, input_top_vendedores=None):
    fig_mapa_receita = px.scatter_geo(
        dados_processados['receita_dos_estados'],
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
        dados_processados['receita_mensal'],
        x='Mes',
        y='Preço',
        markers=True,
        range_y=[0, dados_processados['receita_mensal']['Preço'].max() * 1.1],
        color='Ano',
        line_dash='Ano',
        title='Receita mensal',
    )
    fig_receita_mensal.update_layout(yaxis_title='Receita')

    fig_receita_estados = px.bar(
        dados_processados['receita_dos_estados'].head(),
        x='Local da compra',
        y='Preço',
        title='Receita por estado',
        text_auto=True,
        template='plotly_white',
    )
    fig_receita_estados.update_layout(yaxis_title='Receita')

    fig_receita_categorias = px.bar(
        dados_processados['receita_categorias'],
        text_auto=True,
        title='Receita por categoria',
        template='plotly_white',
    )
    fig_receita_categorias.update_layout(yaxis_title='Receita')

    fig_quantidade_vendas_estados = px.bar(
        dados_processados['quantidade_vendas_estados'],
        x='Local da compra',
        y='Quantidade de Vendas',
        title='Quantidade de vendas por estado',
        text_auto=True,
        template='plotly_white',
    )
    fig_quantidade_vendas_estados.update_layout(yaxis_title='Quantidade de Vendas')

    fig_quantidade_vendas_mensal = px.line(
        dados_processados['quantidade_vendas_mensal'],
        x='Mes',
        y='Quantidade de Vendas',
        markers=True,
        range_y=[0, dados_processados['quantidade_vendas_mensal']['Quantidade de Vendas'].max() * 1.1],
        color='Ano',
        line_dash='Ano',
        title='Quantidade de vendas mensal',
    )
    fig_quantidade_vendas_mensal.update_layout(yaxis_title='Quantidade de Vendas')

    fig_quantidade_vendas_categorias = px.bar(
        dados_processados['quantidade_vendas_categorias'],
        x='Categoria do Produto',
        y='Quantidade de Vendas',
        title='Quantidade de vendas por categoria',
        text_auto=True,
        template='plotly_white',
    )
    fig_quantidade_vendas_categorias.update_layout(yaxis_title='Quantidade de Vendas')

    # input?
    if input_top_vendedores:
        top_vendedores = dados_processados['receita_vendedores'].nlargest(input_top_vendedores, 'sum').reset_index()
        fig_top_vendedores_receita = px.bar(
            top_vendedores,
            x='Vendedor',
            y='sum',
            title=f'Top {input_top_vendedores} vendedores por receita',
            text_auto=True,
            template='plotly_white',
        )
        fig_top_vendedores_receita.update_layout(yaxis_title='Receita')

        fig_top_vendedores_vendas = px.bar(
            top_vendedores,
            x='Vendedor',
            y='count',
            title=f'Top {input_top_vendedores} vendedores por quantidade de vendas',
            text_auto=True,
            template='plotly_white',
        )
        fig_top_vendedores_vendas.update_layout(yaxis_title='Quantidade de Vendas')
    else:
        fig_top_vendedores_receita = None
        fig_top_vendedores_vendas = None

    return {
        'fig_mapa_receita': fig_mapa_receita,
        'fig_receita_mensal': fig_receita_mensal,
        'fig_receita_estados': fig_receita_estados,
        'fig_receita_categorias': fig_receita_categorias,
        'fig_quantidade_vendas_estados': fig_quantidade_vendas_estados,
        'fig_quantidade_vendas_mensal': fig_quantidade_vendas_mensal,
        'fig_quantidade_vendas_categorias': fig_quantidade_vendas_categorias,
        'fig_top_vendedores_receita': fig_top_vendedores_receita,
        'fig_top_vendedores_vendas': fig_top_vendedores_vendas
    }