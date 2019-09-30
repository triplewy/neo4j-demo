
def main():
    f = open("outputacm.txt", "r")
    arr = f.read().split("\n")
    f.close()

    arr = arr[1: len(arr) // 10]

    articles = []
    relatedArticles = []
    authorNames = {}
    authors = []

    currArticle = {}
    currId = None
    tempAuthors = []

    for item in arr:
        if item == '' and currArticle:
            articles.append(currArticle)
            currArticle = {}
            currId = None
        elif item.startswith('#*'):
            currArticle['title'] = item[2:]
        elif item.startswith('#@'):
            for author in item[2:].split(','):
                if author != '':
                    if author not in authorNames:
                        authorNames[author] = len(authorNames)
                    tempAuthors.append(str(authorNames[author]))
        elif item.startswith('#t'):
            currArticle['year'] = item[2:]
        elif item.startswith('#c'):
            currArticle['conference'] = item[2:]
        elif item.startswith('#index'):
            currArticle['id'] = item[6:]
            currId = item[6:]
            for authorId in tempAuthors:
                authors.append({'paperId': currId, 'authorId': authorId})
            tempAuthors = []

        elif item.startswith('#!'):
            currArticle['abstract'] = item[2:]
        elif item.startswith('#%'):
            relatedArticles.append(
                {'paperId': currId, 'relatedId': item[2:]})

    articleStrings = []
    for article in articles:
        row = (
            article['id'],
            article['title'],
            article['year'],
            article['conference'] if 'conference' in article else '',
            # article['abstract'] if 'abstract' in article else ''
        )
        articleStrings.append(";".join(row))

    f = open("articles.csv", "w")
    f.write("id;title;year;conference\n" + "\n".join(articleStrings))
    f.close()

    relatedArticleStrings = []
    for item in relatedArticles:
        relatedArticleStrings.append(item['paperId'] + ';' + item['relatedId'])

    f = open("related.csv", "w")
    f.write("articleId;relatedId\n" + "\n".join(relatedArticleStrings))
    f.close()

    authorStrings = []
    for name, authorId in authorNames.items():
        authorStrings.append(str(authorId) + ';' + name)

    f = open("authors.csv", "w")
    f.write("id;name\n" + "\n".join(authorStrings))
    f.close()

    authorStrings = []
    for item in authors:
        if item['paperId']:
            authorStrings.append(item['paperId'] + ';' + item['authorId'])

    f = open("authorsToArticles.csv", "w")
    f.write("paperId;authorId\n" + "\n".join(authorStrings))
    f.close()


if __name__ == "__main__":
    main()
