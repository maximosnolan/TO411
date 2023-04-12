import yelpapi
client_id = "lyfuVq7zUoXOzMurN4FBqg"
api_key = "4ruotQ7fhv9KWsjYPT9US9vp9JvAehbXIf-cCX3cc7Bc3L_DgaPHcu1-JHvYcFP4eXsyLRp4w3_Ebbx1j0QJqvH57OxL9N72xO-ztGY2KZfIMVZhrTkaroE1Vho0ZHYx"
client = yelpapi.YelpAPI(api_key)
categories = ["Asian", "American", "Italian", "Mexican", "Dessert"]
count = 0
for category in categories:
    while True:
        delivery_results = client.search_query(location='Ann Arbor', limit = 50, offset = count)
        print("MAKING QUEREY FOR", category)
        for business in delivery_results["businesses"]:
            print("-----")
            print("Name:", business["name"])
            print("Rating:", business["rating"])
            print("Category:", business["categories"][0]["title"])
            count +=1
        print("LENGTH", len(delivery_results["businesses"]))
        if len(delivery_results["businesses"]) != 50 or count >= 1000:
            break
