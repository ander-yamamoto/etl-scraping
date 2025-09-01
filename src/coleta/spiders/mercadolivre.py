import scrapy


class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/calcados-roupas-bolsas/calcados/tenis/novo/masculino/tenis-corrida-masculino_FOOTWEAR*TYPE_517583_NoIndex_True"]

    page_count = 1
    max_pages = 10  # Limitar a 5 páginas para evitar scraping excessivo

    def parse(self, response):
        products = response.css('div.poly-card__content')

        for product in products:

            price_block = product.css("div.poly-component__price")

            old_price = None
            current_price = None
            discount = None
            reviews_total = None

            # Preço antigo (tachado com <s>)
            old_block = price_block.css("s.andes-money-amount--previous")
            if old_block:
                frac = old_block.css("span.andes-money-amount__fraction::text").get()
                cents = old_block.css("span.andes-money-amount__cents::text").get()
                old_price = f"{frac}.{cents}" if frac and cents else None

            # Preço atual (dentro de poly-price__current)
            new_block = price_block.css("div.poly-price__current")
            if new_block:
                frac = new_block.css("span.andes-money-amount__fraction::text").get()
                cents = new_block.css("span.andes-money-amount__cents::text").get()
                current_price = f"{frac}.{cents}" if frac and cents else None
                discount = new_block.css("span.andes-money-amount__discount::text").get()

            reviews_total = product.css('span.poly-reviews__total::text').get()
            if reviews_total:
                reviews_total = reviews_total.strip("()")


            yield {
                'brand': product.css('span.poly-component__brand::text').get(),
                'name': product.css('a.poly-component__title::text').get(),
                'old_price': old_price,
                'current_price': current_price,
                'discount': discount,
                'reviews': product.css('span.poly-reviews__rating::text').get(),
                'reviews_total': reviews_total,
            }


        # só continua se ainda não atingiu o limite
        if self.page_count < self.max_pages:
            num_items = len(products)
            if num_items > 0:
                # extrair offset atual
                url = response.url
                if "_Desde_" in url:
                    current_offset = int(url.split("_Desde_")[1].split("_")[0])
                else:
                    current_offset = 1  # primeira página começa do item 1

                next_offset = current_offset + num_items
                next_url = (
                    "https://lista.mercadolivre.com.br/calcados-roupas-bolsas/calcados/tenis/"
                    "novo/masculino/tenis-corrida-masculino_Desde_"
                    f"{next_offset}_FOOTWEAR*TYPE_517583_NoIndex_True"
                )

                # incrementa o contador
                self.page_count += 1

                yield scrapy.Request(next_url, callback=self.parse)



### comandos para rodar o spider e salvar em jsonl
#scrapy startproject coleta 
#scrapy genspider mercadolivre https://lista.mercadolivre.com.br/tenis-corrida-masculino

### comandos para shell
#scrapy shell
#fetch('https://lista.mercadolivre.com.br/tenis-corrida-masculino')
#products=response.css('div.poly-card__content')
#products.css('span.poly-component__brand')