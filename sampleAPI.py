#for complete guide refer to API documentation  here https://developers.google.com/books/docs/v1/using 
import requests
import json
from urllib.request import urlopen
from flask import jsonify

def retrieveBook(isbn):
    url = "https://www.googleapis.com/books/v1/volumes?"
    isbn = isbn.strip()
    res = requests.get(url, 
                   params={ "q": {isbn} })
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")

    bookData = res.json()

    volumeInfo = bookData["items"][0]["volumeInfo"]
    author = volumeInfo["authors"]
    editAuthor = author if len(author) > 1 else author[0]

    # Checking if there are existing ratings
    try: 
        rating = volumeInfo["averageRating"]
        reviewCount = volumeInfo["ratingsCount"]
    except KeyError:
        rating = "Unavailable"
        reviewCount = 0
    
    # Creating dictionary, which will return as JSON object
    bookInfo = {
        "title": volumeInfo['title'],
        "author": editAuthor,
        "year": volumeInfo['publishedDate'][0:4],
        "isbn": isbn,
        "review_count": reviewCount,
        "average_score": rating
    }

    return json.dumps(bookInfo)

if __name__ == "__retrieveBook__":
    retrieveBook()

