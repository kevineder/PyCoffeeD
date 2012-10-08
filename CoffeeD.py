from flask import Flask
from flask import json
from flask import Response
from flask import send_from_directory
from flask import render_template
import ConfigParser
import os
import sys
sys.path.append(sys.path[0]) 
from Scale import Scale
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper


sys.path.append(sys.path[0]) 
Config = ConfigParser.ConfigParser()
Config.read("./config.ini")

VENDOR_ID = 0x6096
PRODUCT_ID = 0x0158

scale = None
app = Flask(__name__)


#Setup crossdomain decorator
def crossdomain(origin=None, methods=None, headers=None,
							max_age=21600, attach_to_all=True,
							automatic_options=True):

	if methods is not None:
			methods = ', '.join(sorted(x.upper() for x in methods))
	if headers is not None and not isinstance(headers, basestring):
			headers = ', '.join(x.upper() for x in headers)
	if not isinstance(origin, basestring):
			origin = ', '.join(origin)
	if isinstance(max_age, timedelta):
			max_age = max_age.total_seconds()

	def get_methods():
			if methods is not None:
					return methods

			options_resp = current_app.make_default_options_response()
			return options_resp.headers['allow']

	def decorator(f):
			def wrapped_function(*args, **kwargs):
					if automatic_options and request.method == 'OPTIONS':
							resp = current_app.make_default_options_response()
					else:
							resp = make_response(f(*args, **kwargs))
					if not attach_to_all and request.method != 'OPTIONS':
							return resp

					h = resp.headers

					h['Access-Control-Allow-Origin'] = origin
					h['Access-Control-Allow-Methods'] = get_methods()
					h['Access-Control-Max-Age'] = str(max_age)
					if headers is not None:
							h['Access-Control-Allow-Headers'] = headers
					return resp

			f.provide_automatic_options = False
			return update_wrapper(wrapped_function, f)
	return decorator

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/grams")
def grams():
	js = json.dumps(round(scale.readGrams(),2))
	resp = Response(js, status=200, mimetype='application/json')
	return resp

@app.route("/ounces")
def ounces():
	js = json.dumps(round(scale.readOunces(),2))
	resp = Response(js, status=200, mimetype='application/json')
	return resp

@app.route("/cups")
def cups():
	js = json.dumps(round(scale.readOunces()/8.0,2))
	resp = Response(js, status=200, mimetype='application/json')
	return resp

@app.route("/servings")
def servings():
	js = json.dumps(round(scale.readOunces()/6.0,2))
	resp = Response(js, status=200, mimetype='application/json')
	return resp

@app.route("/caffeine")
def caffeine():
	js = json.dumps(str(round((scale.readOunces()/8.5)*49,2)) + "mg")
	resp = Response(js, status=200, mimetype='application/json')
	return resp

@app.route("/stats")
@crossdomain(origin='*')
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
@app.route('/418')
def error418():
	return "I'm a tea pot", 418

def getStats():
	return {
		'grams' : round(scale.readGrams(),2), 
		'ounces' : round(scale.readOunces(),2), 
		'cups' : round(scale.readOunces()/8.0,2),
		'servings' : round(scale.readOunces()/6.0,2),
		'caffeine' : str(round((scale.readOunces()/8.5)*49,2)) + "mg"
	}


if __name__ == "__main__":
	scale = Scale(VENDOR_ID, PRODUCT_ID)
	app.debug = True
	app.template_folder="./"
	app.run(host='0.0.0.0')
