from pynytimes import NYTAPI
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv
import datetime
from pynytimes.api import parse_dates
key = "3enKXDylCv5Pje1HA1sGTpcYuTkW0kAT"

nyt = NYTAPI(key, parse_dates = True)


with open("APIAssignment.csv", 'w', newline = "\n") as f:
    companies = ["Ford", "Tesla", "Bloomberg", "Apple", "Microsoft"]
    f.write("date, company, abstract, url, score\n");
    writer = csv.writer(f)
    startDate = datetime.datetime.now() - datetime.timedelta(days=730)
    endDate = datetime.datetime.now()
    dates = {"begin": startDate, "end": endDate}
    for company in companies:

        articles = nyt.article_search(query= company, results= 200, dates = dates)
        print("-----", company, "-----")
        for article in articles:
            analyzer = SentimentIntensityAnalyzer()
            pubDate = article["pub_date"]
            abstract = article["abstract"]
            url = article["web_url"]
            score = analyzer.polarity_scores(abstract)["compound"]
            writer.writerow([pubDate, company, abstract, url,score])
