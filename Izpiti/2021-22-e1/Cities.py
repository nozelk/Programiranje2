import requests
import json
import matplotlib.pyplot as plt
import random

# Preberi vsebino datoteke
url = "https://lovro.fri.uni-lj.si/api/cities"
response = requests.get(url)
data = response.json()

# crno belo
x = [] #sirina
y = [] #dolzina
for slovar in data:
    x.append(float(slovar['lng']))
    y.append(float(slovar['lat']))

plt.scatter(x,y,color='k', marker='o', s=1)
plt.axis('off')
plt.savefig('CBcities.png')

#barvno
x1 = []
y1 = []
drzave={}
barve=[]
for slovar in data:
    drzava=slovar.get('country')
    x1.append(float(slovar['lng']))
    y1.append(float(slovar['lat']))
    if drzava not in drzave:
        drzave[drzava]=[random.random(),random.random(),random.random()]
    barve.append(drzave[drzava])

plt.scatter(x1,y1,c=barve, marker='o', s=1)
plt.axis('off')
plt.savefig('RGBcities.png')    