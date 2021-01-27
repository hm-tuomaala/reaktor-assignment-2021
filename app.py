from flask import Flask, request, render_template
import xml.etree.ElementTree as ET
import requests
import time
from globals import MANUFACTURER_AVAILABILITY

app = Flask(__name__)

API_BASE = "https://bad-api-assignment.reaktor.com"

def find_availability(id, man):
    global MANUFACTURER_AVAILABILITY
    for item in MANUFACTURER_AVAILABILITY[man]:
        if item["id"] == id:
            return ET.fromstring(item["DATAPAYLOAD"]).find("INSTOCKVALUE").text
    return "NOT FOUND"

@app.route("/", methods = ['GET'])
def index():
    return render_template("index.html")

@app.route("/gloves", methods = ['GET'])
def gloves():

    makers = set()
    ret_data = []

    r = requests.get(API_BASE + "/v2/products/gloves")
    if r.status_code != 200:
        return "ERROR"
    data = r.json()

    return render_template("gloves.html", items = data)


@app.route('/background_process_test/<id>/<manufacturer>')
def background_process_test(id, manufacturer):
    print(id.upper(), manufacturer)
    id = id.upper()

    global MANUFACTURER_AVAILABILITY
    if manufacturer in MANUFACTURER_AVAILABILITY.keys():
        print("GLOBAL")
        return find_availability(id, manufacturer)
        print("GLOBAL FAILED")

    print("MAKING REQUEST")
    req = requests.get(API_BASE + "/v2/availability/" + manufacturer)

    if req.status_code != 200 or len(req.json()["response"]) <= 2:
        return "ERROR"

    MANUFACTURER_AVAILABILITY[manufacturer] = req.json()["response"]

    return find_availability(id, manufacturer)


@app.route("/facemasks", methods = ['GET'])
def facemasks():
    return "Facemasks"

@app.route("/beanies", methods = ['GET'])
def beanies():
    return "Beanies"

if __name__ == '__main__':
    app.run(debug=True)
