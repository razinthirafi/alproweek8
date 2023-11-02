import scrapy
import csv

class GamePricesSpider(scrapy.Spider):
    name = 'game_prices'
    start_urls = ['https://store.playstation.com/en-id/category/05a2d027-cedc-4ac0-abeb-8fc26fec7180/1']

    def __init__(self, max_pages=16, *args, **kwargs):
        super(GamePricesSpider, self).__init__(*args, **kwargs)
        self.max_pages = max_pages

    def parse(self, response):
        games = response.css('.psw-t-body.psw-c-t-1.psw-t-truncate-2.psw-m-b-2')
        prices = response.css('.psw-m-r-3')

        # Open the CSV file with proper encoding
        with open('scraped_data.csv', 'a', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            if response.url.endswith('/1'):
                writer.writerow(['title', 'price'])  # Write the header

            for game, price in zip(games, prices):
                title = game.css('span::text').get()
                game_price = price.css('span::text').get()

                # Remove the non-breaking space (U+00A0) characters
                title = title.replace(u'\u00A0', u'')
                game_price = game_price.replace(u'\u00A0', u'')

                writer.writerow([title, game_price])

        # Generate the next page URL based on the pattern
        self.page_number = int(response.url.split('/')[-1]) + 1
        next_page_url = f'https://store.playstation.com/en-id/category/05a2d027-cedc-4ac0-abeb-8fc26fec7180/{self.page_number}'

        # Follow the next page URL
        if self.page_number <= self.max_pages:
            yield response.follow(next_page_url, callback=self.parse)
