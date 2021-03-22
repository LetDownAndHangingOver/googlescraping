from newspaper import Article
url = 'https://telquel.ma/2021/03/05/marche-du-travail-les-inegalites-de-genre-ont-un-cout_1713077'

article = Article(url, language="fr")
article.download()
article.parse()
print('title: ', article.title)

print('author', article.authors)

article.nlp()

print(article.summary)

print(article.keywords)