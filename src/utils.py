def formata_numero(valor, prefixo = ''):
    for unidade in ['', 'Mil']:
        if valor < 1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} Milhões'