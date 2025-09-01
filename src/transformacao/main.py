import pandas as pd
import sqlite3
import datetime
from pathlib import Path


# 1️⃣ Pega o diretório do script principal
BASE_DIR = Path(__file__).parent.resolve()

# 2️⃣ Define a pasta de dados relativa a BASE_DIR
DATA_DIR = BASE_DIR.joinpath('..', '..', 'data').resolve()

# 3️⃣ Garante que a pasta existe (opcional, mas ajuda a evitar erros)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 4️⃣ Define caminhos absolutos para arquivos
JSONL_FILE = DATA_DIR / 'data.jsonl'
DB_FILE = DATA_DIR / 'quotes.db'

# 5️⃣ Lê o JSONL
df = pd.read_json(DATA_DIR / 'data.jsonl', lines=True)

# mostrar todas as colunas
pd.options.display.max_columns = None

# adicionar colunas
df['_source'] = 'https://lista.mercadolivre.com.br/calcados-roupas-bolsas/calcados/tenis/novo/masculino/tenis-corrida-masculino_FOOTWEAR*TYPE_517583_NoIndex_True'
df['_data_coleta'] = datetime.datetime.now()


# tratar os valores nulos para colunas numéricas e de texto

df['old_price'] = pd.to_numeric(df['old_price'], errors='coerce').fillna(0).astype(float)
df['current_price'] = pd.to_numeric(df['current_price'], errors='coerce').fillna(0).astype(float)
df['reviews'] = pd.to_numeric(df['reviews'], errors='coerce').fillna(0).astype(float)
df['reviews_total'] = pd.to_numeric(df['reviews_total'], errors='coerce').fillna(0).astype(int)




# 6️⃣ Conecta no SQLite
conn = sqlite3.connect(DB_FILE)


df.to_sql('mecadolivre_items', conn, if_exists='replace', index=False)

conn.close()

print(df.head(10))