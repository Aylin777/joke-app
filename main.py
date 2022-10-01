from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import pprint

app = FastAPI()
# scrape site
URL = "http://bash.org.pl/latest/?page="
# take first 5 pages, it should be enough to get 100 jokes
req = []
for page in range(1, 6):
    req.append(requests.get(URL + str(page)))
    # req.raise_for_status()

# parse HTML page, sift through it and get the content we need
jokes_list = []
for page in req:
    soup = BeautifulSoup(page.text, "html.parser")
    jokes_dirty_list = soup.find_all('div', class_="quote post-content post-body")
    for j in jokes_dirty_list:
        jokes_list.append(j.text)

pprint.pprint(jokes_list)


# endpoints, dummy for now
@app.get("/")
async def joke_list():
    pprint.pprint(jokes_list)
