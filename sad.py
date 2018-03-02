import requests
import json

a = requests.get("https://us-central1-nbwallet-nb.cloudfunctions.net/getInfo?userId=5901012620037&money=400")
aj = a.json()
print(a, "a")
print(aj['Status'], "aj")