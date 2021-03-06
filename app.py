from flask import Flask, request, render_template
import xml.etree.ElementTree as ET
import requests
import time
from globals import MANUFACTURER_AVAILABILITY

app = Flask(__name__)

API_BASE = "https://bad-api-assignment.reaktor.com"

def find_availability(id, man):
    """
    Parameters
    ----------
    id: str
        id of the product
    man: str
        manufacturer of the product

    Returns
    -------
    str
        returns the availability value of the product
    """
    global MANUFACTURER_AVAILABILITY
    for item in MANUFACTURER_AVAILABILITY[man]:
        if item["id"] == id:
            return ET.fromstring(item["DATAPAYLOAD"]).find("INSTOCKVALUE").text
    return "NOT FOUND"


@app.route("/", methods = ['GET'])
def index():
    """Returns the index page"""
    return render_template("index.html")


@app.route("/gloves", methods = ['GET'])
def gloves():
    """Returns the page for the gloves"""
    r = requests.get(API_BASE + "/v2/products/gloves")
    if r.status_code != 200:
        return "ERROR -- Try reloading the page"
    data = r.json()

    return render_template("gloves.html", items = data)


@app.route("/facemasks", methods = ['GET'])
def facemasks():
    """Returns the page for the facemasks"""
    r = requests.get(API_BASE + "/v2/products/facemasks")
    if r.status_code != 200:
        return "ERROR -- Try reloading the page"
    data = r.json()

    return render_template("facemasks.html", items = data)


@app.route("/beanies", methods = ['GET'])
def beanies():
    """Returns the page for the beanies"""
    r = requests.get(API_BASE + "/v2/products/beanies")
    if r.status_code != 200:
        return "ERROR -- Try reloading the page"
    data = r.json()

    return render_template("beanies.html", items = data)


@app.route('/background_process/<id>/<manufacturer>', methods = ["GET"])
def background_process(id, manufacturer):
    """
    Searches availability info for the requested product.

    Parameters
    ----------
    id: str
        id of the product
    manufacturer: str
        manufacturer of the product

    Returns
    -------
    str
        returns the availability value of the product or 'ERROR' if the API
        request was falty.
    """
    id = id.upper()

    global MANUFACTURER_AVAILABILITY
    if manufacturer in MANUFACTURER_AVAILABILITY.keys():
        return find_availability(id, manufacturer)

    req = requests.get(API_BASE + "/v2/availability/" + manufacturer) # headers = {'x-force-error-mode':'all'}

    if req.status_code != 200 or len(req.json()["response"]) <= 2:
        return "ERROR"

    MANUFACTURER_AVAILABILITY[manufacturer] = req.json()["response"]
    return find_availability(id, manufacturer)


if __name__ == '__main__':
    app.run(debug=True)
