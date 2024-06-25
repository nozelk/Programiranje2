import requests
try:
    html = requests.get("https://www.geeksforgeeks.org/timsort/").text
except requests.exceptions.RequestException as e:
    print(e)
    html = None

print(html)