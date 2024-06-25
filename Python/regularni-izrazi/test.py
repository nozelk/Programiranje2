"""import requests
import re


def igralci():
    req = requests.get('https://en.wikipedia.org/wiki/List_of_Game_of_Thrones_characters')
    page = req.text
    pattern = r'<table class="wikitable.*?</table>'
    tab = re.findall(pattern, page, re.DOTALL)[0]
    tr = re.findall(r"<tr>.*?</tr>",tab,re.DOTALL)[1:]
    print("{:>30s} | {:<30s}".format('Character', 'Actor/Actress'))
    for i in tr:
        vrstice = re.findall(r'<td.*?>.*?</td>',i,re.DOTALL)
        if len(vrstice) >= 2:
            lik = re.findall(r'<a.*?>(.*?)</a>',vrstice[0])[0]
            igralec = re.findall(r'<a.*?>(.*?)</a>',vrstice[1])[0]
            print("{:>30s} | {:<30s}".format(f"'{igralec}", f"'{lik}'"))
    return 0


igralci()"""

import requests

def omdb(naslov, api_key="cd9ba7d7"):
    # Pripravi URL zahteve
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={naslov}"

    
    response = requests.get(url)
    data = response.json()

    
    if data["Response"] == "True":
        print("{:>10s} | '{}' ({})".format("Title", data["Title"], data["Year"]))
        print("{:>10s} | '{}'".format("Genre", data["Genre"]))
        print("{:>10s} | {} ({:,} votes)".format("IMDb", data["imdbRating"], int(data["imdbVotes"].replace(",", ""))))
        print("{:>10s} | '{}'".format("Language", data["Language"]))
        print("{:>10s} | '{}'".format("Country", data["Country"]))
        print("{:>10s} | {} min".format("Runtime", data["Runtime"]))

omdb("The Shawshank Redemption")