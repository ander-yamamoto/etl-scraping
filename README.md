# ETL-Scraping

Pipeline ETL de web scraping usando **Scrapy**, com tratamento de dados em **Pandas** e visualização em **Streamlit**.

Baseado no tutorial: [YouTube: Scrapy + ETL](https://www.youtube.com/watch?v=qNu1VCtUedg&t=607s)

---

## Estrutura do projeto

etl-scraping/  
├── environment.yml # Dependências do conda  
├── README.md  
├── src/  
│ ├── coleta/ # Scrapy spiders  
│ │ └── mercadolivre.py  
│ ├── transformacao/ # Scripts de tratamento de dados  
│ │ └── main.py  
│ └── dashboard/ # Streamlit app  
│ └── app.py  
└── data/ # Arquivos de saída e banco de dados  



---

## Instalação

Clone o repositório e crie o ambiente Conda:

```bash
git clone https://github.com/ander-yamamoto/etl-scraping
cd etl-scraping
conda env create --file environment.yml
conda activate etl-scraping
```
Observação: O environment.yml já inclui todas as dependências necessárias, incluindo Scrapy, Pandas, SQLite e Streamlit.

Uso
1. Coleta de dados com Scrapy
```bash
Copiar código
cd src/coleta
scrapy crawl mercadolivre -o ../data/data.jsonl
```
Isso gera o arquivo data.jsonl com os produtos coletados.

2. Transformação de dados com Pandas
```bash
Copiar código
cd ../transformacao
python main.py
```
O script lê o data.jsonl, aplica transformações e grava no banco de dados quotes.db.

3. Dashboard com Streamlit
```bash
Copiar código
cd ../dashboard
streamlit run app.py
```
Isso inicia o dashboard interativo consumindo os dados processados.

Observações
Certifique-se de estar sempre com o ambiente Conda ativado (conda activate etl-scraping).

Evite scraping excessivo do Mercado Livre para não ser bloqueado.

O pipeline pode ser facilmente automatizado com Airflow, se desejado.