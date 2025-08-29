import newspaper
import validators

# list_of_urls = [ 
#             "https://www.rappler.com/philippines/ethics-complaint-filed-vs-hontiveros-over-alleged-witness-tampering",
#             "https://www.rappler.com/environment/documentary-fish-loss-daram-samar",
#             "https://www.rappler.com/philippines/aspiring-ombudsmen-lifestyle-checks-government-unlike-samuel-martires",
#             "https://www.rappler.com/entertainment/live-jam/music-sessions-young-cocoa-demi-august-2025"
#             ]

# Parse through each url and display its content
class ArticleScraper:
    def article_scraper(self, article_links):
        try:
            from time import sleep
            sleep(1) #delay to avoid limit rates
            article_content = []
            #add valid URL detector
            for url in article_links:
                url_i = newspaper.Article(url="%s" % (url), language='en')
                url_i.download()
                url_i.parse()
                content = (f"TITLE:{url_i.title} CONTENT: {url_i.text}")
                # print(content)
                article_content.append(content)
             
                
            return ("\n".join(article_content))
        except Exception as e:
            return (f"Error occurd: {e}")

# sol = ArticleScraper()
# print(sol.article_scraper(list_of_urls))









