import sys 
import requests
import os
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from bs4 import NavigableString
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS, cross_origin
import tornado.wsgi
import tornado.httpserver
from fashion_parsing import *

curr_dir = os.path.abspath(os.getcwd())
phantomjs_path = os.path.join(curr_dir,'phantomjs/bin/phantomjs')

print(phantomjs_path)
def asos_image_crawler(url):
	driver = webdriver.PhantomJS(phantomjs_path)
	driver.get(url)
	sleep(2)

	html_code = driver.page_source	
	driver.quit()
	result = {}

	print(html_code)
	soup = BeautifulSoup(html_code,'html.parser')	
	print(soup.title.string)
	result['title'] = soup.title.string

	price_tag = soup.find_all('span',{'class':'current-price'})
	fabric_tag = soup.find_all('div',{'class':'about-me'})
	description_tag = soup.find_all('span')
	image_tag = soup.find_all('section',{'id':'core-product'})
	# image_tag = soup.find("meta",  property="og:image")
	for it in image_tag:
		print(it.find_all('img')[0].get('src'))
		result['url']=it.find_all('img')[0].get('src')

	# for pt in price_tag:
	# 	print(pt.contents[0])
	
	#print(price_tag)
	#print(fabric_tag)
	
	#print("Price : " + price_tag[0].contents[0])
	#result['price'] = price_tag[0].contents[0]

	for ft in fabric_tag:
		print(ft.find_all('span')[0].get_text())
		result['material'] = ft.find_all('span')[0].get_text()

	for dt in description_tag:
		if dt.find_all('li')!= []:
			detail = ""
			for x in range(0,len(dt.find_all('li'))-2):
				detail = detail + dt.find_all('li')[x].contents[0] + "  "
			print ("Product detail : " + detail)	
			result['details'] = detail
	
	#result_json = json.dumps(result,indent=4)
	#print(result_json)
	return result

def remove_spaces(contents):
	del_idx = []
	for ind in range(len(contents)):
		if isinstance(contents[ind],NavigableString):
			if len(contents[ind].encode('utf-8').strip()) == 0:
				del_idx.append(ind)

	for ind in sorted(del_idx, reverse=True):
		del contents[ind]

	return contents

def forever21_image_crawler(url):
	html_code = requests.get(url)
	html_code = html_code.text
	#print(html_code)
	soup = BeautifulSoup(html_code,'html.parser')
	men_images = soup.find_all('div',{'id' :'divZoomImage_0'})
	img_tags = soup.find_all('img')
	price_tags = soup.find_all('span')
	description_tags = soup.find_all('section',{'class': 'd_wrapper'})
	product_type = soup.find_all('h1',{'class' : 'item_name_p'})
	result = {}	
		
	for img_tag in img_tags:
		
		if img_tag.get('id')=="ctl00_MainContent_productImage":
			print('Url is: '+img_tag.get('src'))
			print('Alt text: '+img_tag.get('alt'))
			result['url'] = img_tag.get('src')	
	
	
	for men_image in men_images:
		img_tag = men_image.find_all('img')[0]
		result['url'] = img_tag.get('src')
	#	print(men_image.contents[0][1])

	print ("Product type: " + product_type[0].text)
	result['title'] = product_type[0].text
	for price_tag in price_tags:
		if price_tag.get('id')=="priceContainer":
			print(price_tag.contents[0].strip())
			result['price'] = price_tag.contents[0].strip()

	for description_tag in description_tags:
		d_class = description_tag.get('class')
		if d_class is not None:
			if d_class[0] == "d_wrapper":
				
				description_tag.contents = remove_spaces(description_tag.contents)
											
				heading = description_tag.contents[0].get_text()
				
				description = remove_spaces(description_tag.contents[1].contents)[0]
				
				
				if isinstance(description,NavigableString):
					product_detail = description				
				else:
					product_detail = description.get_text()
				
				if heading != 'Size + Fit' and heading!= 'Fit Rating':					
					if heading.lower() =='details':
						result['details'] = product_detail
					if heading == 'Content + Care':
						result['material'] = product_detail
					
	#result_json = json.dumps(result,indent=4)
	#print(result_json)
	return result
				

def hm_image_crawler(url):
	html_code = requests.get(url)
	html_code = html_code.text
	
	soup = BeautifulSoup(html_code,'html.parser')
	image_tags = soup.find_all('div',{'id':'product-image-box'})
	description_tag = soup.find_all('div',{'class':'description'})
	price_tag = soup.find_all('span',{'class' :'actual-price'})
	fabric_tag = soup.find_all('span',{'id':'text-information'})
	heading_tag = soup.find_all('form')[0].find_all('h1')

	result = {}

	for pt in price_tag:
		print("Price: " + pt.contents[0])
		result['price'] = pt.contents[0]

	for ht in heading_tag:
		print("Clothing item: " + ht.contents[0].strip())
		result['title'] = ht.contents[0].strip()

	for dt in description_tag:
		print("Description: " + dt.contents[5].get_text().strip())
		result['details'] = dt.contents[5].get_text().strip()
		
	for ft in fabric_tag:
		print("Fabric description: " + ft.contents[0])
		result['material'] = ft.contents[0]
	
	for image_tag in image_tags:
		img_tag = image_tag.find_all('img')
		print (img_tag[0].get('src').lstrip('//'))
		result['url'] = 'http://' + img_tag[0].get('src').lstrip('//')
		print(result['url'])

	#result_json = json.dumps(result,indent=4)
	#print(result_json)
	return result

def image_crawler(url,crawler_type):
	if crawler_type =="hm":
		result = hm_image_crawler(url)
	if crawler_type == "forever21":
		result = forever21_image_crawler(url)
	if crawler_type == "asos":
		result = asos_image_crawler(url)

	return result

	
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
		url = request.args['url']

		if url.find("asos.com") != -1:
			crawler_type = "asos"	    
			result = image_crawler(url,crawler_type)
		if url.find("hm.com") != -1:
			crawler_type = "hm"	    
			result = image_crawler(url,crawler_type)
		if url.find("forever21.com") != -1:
			crawler_type = "forever21"	    
			result = image_crawler(url,crawler_type)
	
		if 'url' in result and len(result['url'])>0:
			try:
				image_url = result['url']
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
