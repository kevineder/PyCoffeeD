from flask import Flask
from flask import json
from flask import Response
from flask import send_from_directory
from flask import render_template
import os

import sys
sys.path.append(sys.path[0]) 
from Scale import Scale

VENDOR_ID = 0x6096
PRODUCT_ID = 0x0158

scale = None
app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html', stats=getStats())

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

@app.route("/servings")
def servings():
	js = json.dumps(scale.readOunces()/6.0)
	resp = Response(js, status=200, mimetype='application/json')
	return resp

@app.route("/caffeine")
def caffeine():
	js = json.dumps(str(round((scale.readOunces()/8.5)*49,2)) + "mg")
	resp = Response(js, status=200, mimetype='application/json')
	return resp

@app.route("/stats")
def stats():
	stats = getStats()

	js = json.dumps(stats)
	resp = Response(js, status=200, mimetype='application/json')
	return resp

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),
		'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.errorhandler(418)
def error418():
	return "I am a tea pot"

def getStats():
	return {
		'grams' : scale.readGrams(), 
		'ounces' : scale.readOunces(), 
		'cups' : scale.readOunces()/8.0,
		'servings' : scale.readOunces()/6.0,
		'caffeine' : str(round((scale.readOunces()/8.5)*49,2)) + "mg"
	}

if __name__ == "__main__":
	scale = Scale(VENDOR_ID, PRODUCT_ID)
	app.debug = True
	app.run(host='0.0.0.0')
