import requests
from flask import jsonify

body = {"query": 'query { promotion (code:"testmsg") {name, start, end}}'}
r = requests.post("http://127.0.0.1:5100/graphql", json = body)

print(r.json())