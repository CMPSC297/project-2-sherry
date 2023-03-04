# Google Books API Documentation: https://developers.google.com/books/docs/v1/using 

import requests
import json
from flask import jsonify

def retrieveBook(isbn):
    url = "https://www.googleapis.com/books/v1/volumes?"
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

def retrieveAverageRating(isbn):
    url = "https://www.googleapis.com/books/v1/volumes?"
    res = requests.get(url, 
                   params={ "q": {isbn} })
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")

    bookData = res.json()
    volumeInfo = bookData["items"][0]["volumeInfo"]

    # Checking if there are existing ratings
    try: 
        rating = volumeInfo["averageRating"]
    except KeyError:
        rating = "Unavailable"
    
    reviewInfo = "Average Rating: {}".format(rating)

    return reviewInfo


def retrieveNumberOfRating(isbn):
    url = "https://www.googleapis.com/books/v1/volumes?"
    res = requests.get(url, 
                   params={ "q": {isbn} })
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")

    bookData = res.json()
    volumeInfo = bookData["items"][0]["volumeInfo"]

    # Checking if there are existing ratings
    try: 
        reviewCount = volumeInfo["ratingsCount"]
    except KeyError:
        reviewCount = 0
    
    reviewInfo = "Number of Ratings: {}".format(reviewCount)

    return reviewInfo
