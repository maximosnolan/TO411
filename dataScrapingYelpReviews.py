import yelpapi
import requests
import csv
from bs4 import BeautifulSoup
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

PIVOT_MACRO = 132
MAX_NUMBER_LOCATIONS_PER_CATAGORY = 1000
RATE_LIMIT = 50

#TODO: We should each take one city to compound results, just change this and let the script run.
CITY = "Ann Arbor"

def determineSentiment(business_id: str) -> float:
    url = f'https://www.yelp.com/biz/{business_id}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    review_container = soup.find_all('div', {'class': 'border-color--default__09f24__NPAKY'})
    #No reviews exist, default to 0
    if len(review_container) < PIVOT_MACRO:
        return 0.0
    allReviews = review_container[PIVOT_MACRO].text
    numReviews = 0
    accumulator = 0
    for review in allReviews.split("."):
        analyzer = SentimentIntensityAnalyzer()
        accumulator += analyzer.polarity_scores(review)["compound"]
        numReviews += 1
    return accumulator / numReviews



def main():
    api_key = "4ruotQ7fhv9KWsjYPT9US9vp9JvAehbXIf-cCX3cc7Bc3L_DgaPHcu1-JHvYcFP4eXsyLRp4w3_Ebbx1j0QJqvH57OxL9N72xO-ztGY2KZfIMVZhrTkaroE1Vho0ZHYx"
    client = yelpapi.YelpAPI(api_key)
    categories = ["Asian", "American", "Italian", "Mexican", "Dessert"]
    with open("reviewsFor" + CITY + ".csv", 'w', newline = "\n") as f:
        f.write("name, id, location, rating, category, score\n")
        writer = csv.writer(f)
        for category in categories:
            count = 0
            while True:
                delivery_results = client.search_query(location= CITY, limit = RATE_LIMIT, offset = count)
                print("querey for...", category)
                for business in delivery_results["businesses"]:
                    print("-----")
                    print("Name:", business["name"])
                    print("ID:", business["id"])
                    print("Location:", CITY)
                    print("Rating:", business["rating"])
                    print("Category:", business["categories"][0]["title"])
                    score = determineSentiment(str(business["id"]))
                    print("sentiment score: ", score)
                    writer.writerow([business["name"], business["id"], CITY, business["rating"], business["categories"][0]["title"], score])
                    count +=1
                if len(delivery_results["businesses"]) != RATE_LIMIT or count >= MAX_NUMBER_LOCATIONS_PER_CATAGORY:
                    print("FINISHED JOB FOR", category, "WITH", count, "RESULTS.\n")
                    break



if __name__ == "__main__":
    main()
