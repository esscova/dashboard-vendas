import plotly.express as px

def cria_graficos(dados_processados, input=5):
    receita_dos_estados = dados_processados['receita_dos_estados']
    receita_mensal = dados_processados['receita_mensal']
    receita_categorias = dados_processados['receita_categorias']
    receita_vendedores = dados_processados['receita_vendedores']

    fig_mapa_receita = px.scatter_geo(
        receita_dos_estados,
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
        receita_mensal,
        x='Mes',
        y='Preço',
        markers=True,
        range_y=[0, receita_mensal['Preço'].max() * 1.1],
        color='Ano',
        line_dash='Ano',
        title='Receita mensal',
    )
    fig_receita_mensal.update_layout(yaxis_title='Receita')

    fig_receita_estados = px.bar(
        receita_dos_estados.head(),
        x='Local da compra',
        y='Preço',
        title='Receita por estado',
        text_auto=True,
        template='plotly_white',
    )
    fig_receita_estados.update_layout(yaxis_title='Receita')

    fig_receita_categorias = px.bar(
        receita_categorias,
        text_auto=True,
        title='Receita por categoria',
        template='plotly_white',
    )
    fig_receita_categorias.update_layout(yaxis_title='Receita')

    fig_receita_vendedores = px.bar(
        receita_vendedores[['sum']].sort_values(by='sum', ascending=False).head(input),
        x='sum',
        y=receita_vendedores[['sum']].sort_values(by='sum', ascending=False).head(input).index,
        title='Receita por vendedor',
        text_auto=True,
        template='plotly_white',
    )
    fig_receita_vendedores.update_layout(yaxis_title='Receita')

    return {
        'fig_mapa_receita': fig_mapa_receita,
        'fig_receita_mensal': fig_receita_mensal,
        'fig_receita_estados': fig_receita_estados,
        'fig_receita_categorias': fig_receita_categorias,
        'fig_receita_vendedores': fig_receita_vendedores
    }