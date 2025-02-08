import streamlit as st
def formata_numero(valor, prefixo = ''):
    for unidade in ['', 'Mil']:
        if valor < 1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} Milhões'

styles = """
    <style>
        .card {
            box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
            transition: 0.3s;
            border-radius: 10px;
            padding: 20px;
            background-color: white;
            margin-bottom: 20px;
        }
        .card:hover {
            box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
        }
        .contact-badge {
            padding: 0.8rem;
            margin: 0.5rem 0;
            border-radius: 8px;
            background-color: #D6D8DC;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .contact-badge:hover {
            transform: translateX(5px);
            background-color: #e3e8f2;
        }
    </style>
"""

def card(titulo, df):
    return st.markdown(f"""
        <div class=card>
                <h3>{titulo}</h3>
                <h2>{formata_numero(df)}</h2>
        </div>""", unsafe_allow_html=True)

contato = """
    <div>
        <h3>Contatos</h3>
        <div class="contact-badge">
            <a href="https://github.com/esscova" target="_blank" style="text-decoration:none; color:#2c3e50;">
            💻 GitHub
            </a>
        </div>
        <div class="contact-badge">
            <a href="https://linkedin.com/in/wellington-moreira-santos" target="_blank" style="text-decoration:none; color:#2c3e50;">
            💼 LinkedIn
            </a>
        </div>
    </div>
"""