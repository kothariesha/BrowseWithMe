import sys 
import requests
import os
import json
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS, cross_origin
import tornado.wsgi
import tornado.httpserver
from fashion_parsing import *

app = Flask(__name__)
CORS(app)
def start_tornado(app, port=5000):
    http_server = tornado.httpserver.HTTPServer(
        tornado.wsgi.WSGIContainer(app))
    http_server.listen(port)
    print("Tornado server starting on port {}".format(port))
    tornado.ioloop.IOLoop.instance().start()

 
@app.route("/BrowseWithMe")
def api_BrowseWithMe():
	result = {}
	if 'url' in request.args:
		image_url = request.args['url']
		try:
			im_path = download_image(image_url,300)
			result = segment_image(im_path,image_url,result)
			
			#json_str = json.loads(json.dumps(result))
			#print(json.dumps(json_str, indent=4, sort_keys=True))
			print("Computer vision done")
		except:
			print("Computer vision failed")

	else:    	
		print("No url from client")

	return jsonify([result])    
 
if __name__ == "__main__":
    start_tornado(app, 5000)
