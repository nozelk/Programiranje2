"""import requests
import json
import matplotlib.pyplot as plt

def cena_srebra():

    url = 'http://www.dmfa-zaloznistvo.si/matjaz/prog2-pra/srebro.txt'


    response = requests.get(url)
    data = json.loads(response.text)


    dates = [entry["date"] for entry in data]
    highs = [entry["high"] for entry in data]
    lows = [entry["low"] for entry in data]


    plt.figure(figsize=(10, 6))
    plt.plot(dates, highs, label="Najvišja cena", color="blue")
    plt.plot(dates, lows, label="Najnižja cena", color="orange")
    plt.fill_between(dates, lows, highs, color="gray", alpha=0.3)
    plt.xlabel("Datum")
    plt.ylabel("Cena srebra")
    plt.title("Gibanje najvišje in najnižje dnevne cene srebra (31.10.2018 - 30.10.2019)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()


    plt.savefig("srebro.png")
    plt.show()

cena_srebra()"""
import requests
import json
import matplotlib.pyplot as plt

def cena_srebra():

    url = 'http://www.dmfa-zaloznistvo.si/matjaz/prog2-pra/srebro.txt'

    response = requests.get(url)
    data = json.loads(response.text)

    dates = [entry["date"] for entry in data]
    highs = [entry["high"] for entry in data]
    lows = [entry["low"] for entry in data]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, highs, label="Najvišja cena", color="blue")
    plt.plot(dates, lows, label="Najnižja cena", color="orange")
    plt.fill_between(dates, lows, highs, color="gray", alpha=0.3)
    plt.xlabel("Datum")
    plt.ylabel("Cena srebra")
    plt.title("Gibanje najvišje in najnižje dnevne cene srebra (31.10.2018 - 30.10.2019)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()

    
    plt.xticks([])

    plt.savefig("srebro.png")
    plt.show()

cena_srebra()

