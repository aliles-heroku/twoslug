import requests


BASE = "http://api.duckduckgo.com/?q={0}&format=json&t=twoslug"

def define(word):
    req = requests.get(BASE.format("define+" + word))
    definition = req.json()
    if len(definition["Definition"]) == 0:
            req = requests.get(BASE.format(word))
            definition = req.json()
    definition.update(ApiSource='DuckDuckGo', ApiURL='https://duckduckgo.com/')
    return definition
