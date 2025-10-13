# from newspaper import Article

# # URL of the article you want to scrape
# url = "https://www.rappler.com/philippines/ethics-complaint-filed-vs-hontiveros-over-alleged-witness-tampering"

# # Create an Article object with the given URL and language (e.g., 'en' for English)
# toi_article = Article(url, language="en")

# # To download the article
# toi_article.download()

# # To parse the article (i.e., extract the content)
# toi_article.parse()

# # To extract the article's title
# print("Article's Title:")
# print(toi_article.title)
# print("\n")
# # To extract the article's full text
# print("Article's Text:")
# print(toi_article.text)
# print("\n")


# art_list = [ 
#             "https://www.rappler.com/philippines/ethics-complaint-filed-vs-hontiveros-over-alleged-witness-tampering",
#             "https://www.rappler.com/environment/documentary-fish-loss-daram-samar",
#             "https://www.rappler.com/philippines/aspiring-ombudsmen-lifestyle-checks-government-unlike-samuel-martires",
#             "https://www.rappler.com/entertainment/live-jam/music-sessions-young-cocoa-demi-august-2025"
#             ]



# # art_list = "https://www.rappler.com/philippines/ethics-complaint-filed-vs-hontiveros-over-alleged-witness-tampering"
# from newspaper import Article
# class BetterScraper:

#     def scrape_articles(self, article_urls):
#         article = Article(article_urls, language="en")
#         for _ in range(len(article_urls)):
#             article.download()
#             article.parse()
#         print(article.text)




# value = BetterScraper()
# value.scrape_articles(art_list)


# Import required modules
# import newspaper

# # Define list of urls
# list_of_urls = [ 
#             "https://www.rappler.com/philippines/ethics-complaint-filed-vs-hontiveros-over-alleged-witness-tampering",
#             "https://www.rappler.com/environment/documentary-fish-loss-daram-samar",
#             "https://www.rappler.com/philippines/aspiring-ombudsmen-lifestyle-checks-government-unlike-samuel-martires",
#             "https://www.rappler.com/entertainment/live-jam/music-sessions-young-cocoa-demi-august-2025"
#             ]

# # Parse through each url and display its content
# class ArticleScraper:
#     def __init__(self):
#         pass
    
#     def articleScraper(self, article_links):
#         article_content = []
#         for url in article_links:
#             url_i = newspaper.Article(url="%s" % (url), language='en')
#             url_i.download()
#             url_i.parse()
#             content = (f"TITLE:{url_i.title} ARTICLES: {url_i.text}")
#             # print(content)
#             article_content.append(content)
        
#         return ("\n".join(article_content))

# sol = ArticleScraper()
# print(sol.articleScraper(list_of_urls))

import validators

print(validators.url("http://google.com"))