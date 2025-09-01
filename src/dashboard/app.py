import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

# diretório base e pasta de dados
BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR.joinpath('..', '..', 'data').resolve()
DATA_DIR.mkdir(parents=True, exist_ok=True)

# caminhos absolutos para arquivos
JSONL_FILE = DATA_DIR / 'data.jsonl'
DB_FILE = DATA_DIR / 'quotes.db'


# conectar ao banco de dados SQLite
conn = sqlite3.connect(DB_FILE)


# carregar os dados da tabela
df = pd.read_sql_query("SELECT * FROM mecadolivre_items", conn)

# fechar a conexão
conn.close()

# titulo da aplicação
st.title("Pesquisa de Mercado - Tenis de Corrida no Mercado Livre")
st.subheader("KPIs principais do sistema")


col1, col2, col3 = st.columns(3)

# kpi 1 - total de produtos
total_products = len(df)
col1.metric("Total de Produtos", total_products)

# kpi 2 - preço médio atual
unique_brands = df['brand'].nunique()
col2.metric("Marcas Únicas", unique_brands)

# kpi 3 - preço médio atual
average_current_price = df['current_price'].mean()
col3.metric("Preço Médio Atual (R$)", f"{average_current_price:.2f}")

# quais marcas são as mais encontradas até a pagina 10?
st.subheader("Marcas mais encontradas até a página 10")
col1, col2 = st.columns([4,2])

top_10_pages_brands = df['brand'].value_counts().sort_values(ascending=False).head(10)
col1.bar_chart(top_10_pages_brands)
col2.write(top_10_pages_brands)


# preço médio atual por marca
st.subheader("Preço Médio Atual por Marca")
col1, col2 = st.columns([4,2])
avg_price_per_brand = df.groupby('brand')['current_price'].mean().sort_values(ascending=False)
col1.bar_chart(avg_price_per_brand)
col2.write(avg_price_per_brand)


# satisfação dos usuários (reviews)
st.subheader("Satisfação dos Usuários (Reviews)")
col1, col2 = st.columns([4,2])
df_temp = df[df['reviews_total'] > 0]  # filtrar apenas produtos com reviews
avg_reviews_per_brand = df_temp.groupby('brand')['reviews'].mean().sort_values(ascending=False)
col1.bar_chart(avg_reviews_per_brand)
col2.write(avg_reviews_per_brand)