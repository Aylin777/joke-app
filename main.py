from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import pickle
import pprint

app = FastAPI()
# scrape site
URL = "http://bash.org.pl/latest/?page="
# take first 5 pages, it should be enough to get 100 jokes
for page in range(1, 6):
    file = (requests.get(URL + str(page)))
    # it would be nice to handle errors ie when page is unavailable
    # req.raise_for_status()

    # save scraped pages to file, it's not nice to overload someone's page with requests
    try:
        f = open("jokes"+str(page)+".html", "wb")
        pickle.dump(file, f)
        f.close()
    except FileNotFoundError:
        with open("jokes"+str(page)+".html", "wb") as f:
            pickle.dump(file, f)
        f.close()

# parse saved pages, sift through them and get the content we need
jokes_list = []
for page in range(1, 6):
    with open("jokes"+str(page)+".html", "rb") as file:
        soup = BeautifulSoup(file, "html.parser")
        jokes_dirty_list = soup.find_all('div', class_="quote post-content post-body")
        for j in jokes_dirty_list:
            jokes_list.append(j.text)
        file.close()

pprint.pprint(jokes_list)


# endpoints, dummy for now
@app.get("/")
async def joke_list():
    pprint.pprint(jokes_list)
