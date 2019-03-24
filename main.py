import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint

pollies = dict()


def getLib():
    # get all the liberal MPs
    print("Loading all the Liberal MPs")
    libearl = requests.get("https://nsw.liberal.org.au/Our-People/State-Liberals")
    newSoup = BeautifulSoup(libearl.content, 'html.parser')
    libearlMps = newSoup.find("ul", {"class": "thumbnails liberals-section"})
    LiberalLinks = libearlMps.findAll("a")
    tovisit = []
    for liblink in LiberalLinks:
        if "/Members/" in liblink.get('href'):
            tovisit.append(liblink.get('href'))
    i = 1
    for liberals in tovisit:
        print(liberals, i, len(tovisit))
        cursite = "https://nsw.liberal.org.au" + liberals
        currentMP = requests.get(cursite)
        tempSoup = BeautifulSoup(currentMP.content, 'html.parser')
        #le le-post_content
        pageContent = tempSoup.find("div", {"class": "le-post_content"})
        pollies[cursite] = str(pageContent.get_text()).lower()
        i= i+1

    # Get all the Labour MPs
def getLab():
    print("Loading all the Labour MPs")
    labour = requests.get("https://www.michaeldaley.com.au/our_team")
    soup = BeautifulSoup(labour.content, 'html.parser')
    labourMPs = soup.find("div", {"id": "mix_it_up_posts"})
    links = labourMPs.findAll("a")
    labours = []
    for link in links:
        cur = link.get('href')
        if cur not in labours:
            labours.append(cur)
    i = 1
    for labourMp in labours:
        print(labourMp, i, len(labours))
        cursite = "https://www.michaeldaley.com.au/" + labourMp
        curMP = requests.get(cursite)
        oldSoup = BeautifulSoup(curMP.content, 'html.parser')
        #col-md-12 pt-4
        pageContent = oldSoup.find("div", {"class": 'col-md-12 pt-4'})

        pollies[cursite] = str(pageContent.get_text()).lower()
        i = i+1




def refreshData():
    getLib()
    getLab()
    with open('mpData.json', 'w') as fp:
        json.dump(pollies, fp)

def searchDataset(term,json):
    for pollie in json:
        found = False
        if term.capitalize() in json[pollie]:
            found = True
        if term in json[pollie]:
            found = True

        if found:
            print(pollie)
            print(json[pollie])

if __name__ == "__main__":
    refresh = input("Should I refresh my dataset?:")
    if "yes" in refresh:
        refreshData()
    try:
        f = open('mpData.json')
    except IOError:
        print("Couldnt find file, doing it for myself")
        refreshData()
        f = open ("mpData.json")
    with f:
        mpData = json.load(f)
    while True:
        current = input ("What do you want to search for (Type quit to stop):")
        if "quit" in current:
            break
        searchDataset(current, mpData)
