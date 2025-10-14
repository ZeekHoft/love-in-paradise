import newspaper


list_of_urls = [
           
            "https://www.bworldonline.com/top-stories/2025/09/05/695808/ng-outstanding-debt-surges-to-record-p17-56-trillion-as-of-end-july",
            "https://www.rappler.com/life-and-style/relationships/two-pronged-ghosted-someone-feeling-guilty-confused/",
            "https://www.rappler.com/environment/philippines-renewable-sector-races-meet-targets-coal-plants-linger-lng-grows/"
            ]




class ArticleScraper:
    
        def __init__(self):
            self.links_data = {}
        
        def article_scraper(self, article_links):
            try:
                for url in article_links:
                    artcile = newspaper.article(url="%s" % (url), language="en")
                    artcile.download()
                    artcile.parse()
                
                    self.links_data[url] = {
                        "headline": artcile.title,
                        "content": artcile.text,
                        #add more specific data to retreive, date, author etc...
                    }
                return self.links_data

            except Exception as e:
                return f"Error in scraping {e}"



scrape = ArticleScraper()
print(scrape.article_scraper(list_of_urls))
