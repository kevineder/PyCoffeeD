from flask import Flask
from flask import json
from flask import Response

import sys
sys.path.append(sys.path[0]) 
from coffeed import Scale

VENDOR_ID = 0x6096
PRODUCT_ID = 0x0158

scale = None
app = Flask(__name__)

@app.route("/")
@app.route("/grams")
def grams():
	js = json.dumps(scale.readGrams())
	resp = Response(js, status=200, mimetype='application/json')
	return resp

@app.route("/ounces")
def ounces():
	js = json.dumps(scale.readOunces())
	resp = Response(js, status=200, mimetype='application/json')
	return resp

@app.route("/cups")
def cups():
	js = json.dumps(scale.readOunces()/8.0)
	resp = Response(js, status=200, mimetype='application/json')
	return resp

if __name__ == "__main__":
	scale = Scale(VENDOR_ID, PRODUCT_ID)
	app.run(host='0.0.0.0')

