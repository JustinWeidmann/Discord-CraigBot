from bs4 import BeautifulSoup
import requests

def runScrape(QUERY):
    BASE_URL = 'https://denver.craigslist.org'
        
    def stepThroughPages(posts, pageLink):  #Recursion function - Grabs all page data
        source = requests.get(BASE_URL + pageLink).text
        soup = BeautifulSoup(source, 'html.parser')
        nextButton = soup.find('a', class_='button next')
        posts.extend(soup.find_all('li', 'result-row'))


        if nextButton is None: return posts
        return stepThroughPages(posts, nextButton.get('href'))

    def outputResults(posts):
        resultIndex = []
        resultTitle = []
        resultTime = []
        resultLocation = []
        resultURL = []
        for i, post in enumerate(posts):
            postTitle = post.find('a', class_='result-title').get_text()
            postTime = post.find('time', class_='result-date').get('datetime')
            postPreLocation = post.find('span', class_='result-hood')
            if postPreLocation is None:
                postLocation = "(¯\_(ツ)_/¯)"   #IDK bro ¯\_(ツ)_/¯
            else:
                postLocation = postPreLocation.get_text()
            postURL = post.find('a', class_='result-title').get('href')

            #print(f'{i}: {postTitle}\n {postTime}\n {postLocation}\n {postURL}\n')
            
            resultIndex.append(i)
            resultTitle.append(postTitle)
            resultTime.append(postTime)
            resultLocation.append(postLocation)
            resultURL.append(postURL)
        return resultIndex, resultTitle, resultTime, resultLocation, resultURL
            

    totalPosts = stepThroughPages([], '/search/zip')

    totalQueryPosts = [post for post in totalPosts if QUERY in post.find('a', class_='result-title').get_text().lower()]    #List comprehension - Sorts for metal(or whatever you want)
    print(f'{len(totalQueryPosts)} results containing "{QUERY}"')

    scrapeResults = outputResults(totalQueryPosts)

    postPercentage = round((len(totalQueryPosts) / len(totalPosts) * 100), 1)
    funFact = f'{len(totalQueryPosts)} of the total {len(totalPosts)} free posts contained {QUERY}. Thats {postPercentage}%!'
    print(funFact)

    return scrapeResults, funFact

#cregResults = runScrape("metal")
#print(cregResults)