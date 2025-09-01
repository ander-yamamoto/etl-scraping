# ETL-Scraping


ETL Pipeline for price scraping base on tutorial:
https://www.youtube.com/watch?v=qNu1VCtUedg&t=607s


Instructions

```
git clone https://github.com/ander-yamamoto/etl-scraping
cd etl-scraping
conda env create --file environment.yml
conda activate etl-scraping
```

scrapy genspider mercadolivre https://lista.mercadolivre.com.br/tenis-corrida-masculino
fetch('https://lista.mercadolivre.com.br/tenis-corrida-masculino')
products=response.css('div.poly-card__content')
products.css('span.poly-component__brand')