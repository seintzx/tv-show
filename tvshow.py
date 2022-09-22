import requests
import json
import time
import os
import re

APIKEY = ""

def getID(APIKEY, title):
    try:
        # use https://imdb-api.com/en/API/SearchSeries/{}/{} if null use Search only
        URL = "https://imdb-api.com/en/API/Search/{}/{}".format(APIKEY, title)
        res = requests.get(URL).json()
        res = res["results"][0]["id"]
    except Exception as err:
        print("ID error: {}".format(err))
        res = ""
    return(res)

def getInfo(APIKEY, id):
    try:
        URL = "https://imdb-api.com/en/API/Title/{}/{}".format(APIKEY, id)
        res = requests.get(URL).json()
    except Exception as err:
        print("INFO error: {}".format(err))
        res = ""
    return(res)

def getDir(directory):
    all = []
    for filename in os.listdir(directory):
        all.append(filename[:-3])
    return(all)

def getList(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        lines.sort()
        f.close()
    return(lines)

def createShow(directory, show):
    res = ""
    newFile = os.path.join(directory, "{}.md".format(show))
    with open(newFile, 'w') as f:
        ID = getID(APIKEY, show.replace('_', ' '))
        infos = getInfo(APIKEY, ID)
        title = infos["title"] if infos["title"] is not None else "Broken Title for {}".format(show)
        print("Building plot for {}..".format(title))
        plot = infos["plot"].replace(". ", ".\n") if infos["plot"] is not None else "Broken Plot"
        genres = infos["genres"] if infos["genres"] is not None else "Broken Genres"
        res += "### {}\n\n".format(title)
        res += "Genres: {}\n\n".format(genres)
        res += "{}\n\n".format(plot)
        f.write(res)
        f.close()

def buildReadme(directory):
    with open("template/ranking.md", 'r') as f:
        all = f.read()
        f.close()
    for filename in os.listdir(directory):
        namefile = os.path.join(directory, filename)
        with open(namefile, 'r') as f:
            all += "{}".format(f.read())
            f.close()
    with open("README.md", 'w') as f:
        f.write(all)
        f.close()

def main():
    directory = "shows"
    dirShows = getDir(directory)
    listShows = [
        re.sub(r"\W+", '',
               show.lower().replace(' ', '_')).strip()
        for show in getList("template/showlist.md")
    ]
    for show in listShows:
        if show not in dirShows:
            createShow(directory, show)
            time.sleep(10)
    buildReadme(directory)

if __name__ == "__main__":
    main()
