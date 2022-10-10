import pandas as pd

import geopandas as gpd
from shapely.geometry import Point,Polygon

import requests
import pprint 
import json

url = "https://eonet.gsfc.nasa.gov/api/v3/events"

output = 'json'
#print( f'{url}?format={output}' )

# get a response using https
def httpget():
    """get data from http

    Returns:
        json: geojson data
    """
    response = requests.get(
    f'{url}?format={output}',verify=False
    ).json()

    return response

def readfile():
    """reads debug.json

    Returns:
        json: geojson data
    """
    f = open('debug.json')
    data = json.load(f)
    f.close()
    return data

response = readfile() # httpget()

def debugwrite(response:dict):
    """write the data to debug.json

    Args:
        json (dict): geojson data from httpget()
    """
    jsonString = json.dumps(response,indent=4)
    jsonFile = open("debug.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()


a = httpget()
debugwrite(a)
# pprint.pprint(response)
print(31)