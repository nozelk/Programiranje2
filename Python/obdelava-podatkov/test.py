import requests

def matematiki(izhod):
    url = "http://www.dmfa-zaloznistvo.si/matjaz/prog2-pra/matematiki.txt"
    response = requests.get(url)

    linije = response.text.splitlines()[1:]
    slo = dict()
    for i in linije:
        vrstica = i.split("\t")
        ime_priimek = vrstica[0] + " " + vrstica[1]
        id = vrstica[2]
        if id not in slo.keys():
            slo[id] = {"ime_priimek": ime_priimek,"min_leto" : min(float("inf"), int(vrstica[13])), "max_leto": max(float("-inf"), int(vrstica[13])), "tocke": 0 if vrstica[22] == "NA" else float(vrstica[22]), "raziskave" : 1}
        else:
            slo[id]["tocke"] += 0 if vrstica[22] == "NA" else float(vrstica[22])
            slo[id]["raziskave"] += 1
            slo[id]["min_leto"] = min(slo[id]["min_leto"], int(vrstica[13]))
            slo[id]["max_leto"] = max(slo[id]["max_leto"], int(vrstica[13]))
    s = dict()
    for i in slo.values():
        tocke = i["tocke"]
        publ = i["raziskave"]
        leta = i["max_leto"] - i["min_leto"] + 1
        s[i["ime_priimek"]] = [float(publ / leta), float(tocke / leta)]
    s = dict(sorted(s.items(), key=lambda item: item[1][1], reverse=True))
    
    with open(izhod, "w", encoding="ISO-8859-1") as dat2:
            for k, v in s.items():
                dat2.write(f"{k}\t{v[0]:.2f}\t{v[1]:.2f}\n")
    return izhod


print(matematiki("izhodna.txt"))