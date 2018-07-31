import sys
import os
import fnmatch
import time
import json
import datetime

caffe_root = '/home/suyog/software/deeplab-public-ver2/distribute/'
sys.path.insert(0, caffe_root + 'python')
import caffe
import numpy as np
from PIL import Image
from extract_colors import *

caffe_model = os.path.join(os.getcwd(),'model','fashion_parsing.caffemodel')
proto_file  = os.path.join(os.getcwd(),'model','fashion_parsing.prototxt')

description_labels = ['Hat','Sunglasses','Top','Skirt','Pants', 'Dress', 'Belt', 'Bag','Scarf'];

USE_GPU = False

if USE_GPU == True:
	caffe.set_device(0)
	caffe.set_mode_gpu()
else:
	caffe.set_mode_cpu()

net = caffe.Net(proto_file,caffe_model,caffe.TEST)

colormap_file = os.path.join(os.getcwd(),'model','pascal_seg_colormap.mat')
color_lab_matrix_path = os.path.join(os.getcwd(),'model','xkcd-lab-matrix.pk')
color_names_path = os.path.join(os.getcwd(),'model','xkcd-lab-colors.pk')

UPLOAD_FOLDER = os.path.join(os.getcwd(),'images')
ALLOWED_IMAGE_EXTENSIONS = set(['png', 'bmp', 'jpg', 'jpe', 'jpeg', 'gif'])

def download_image(image_url,max_size):
	filename_ = str(datetime.datetime.now()).replace(' ', '_') + '_image.jpg'
	im_path = os.path.join(UPLOAD_FOLDER,filename_)
	print(im_path);
	cmd = 'wget -O '+im_path+ ' "' + image_url + '"'
	os.system(cmd)

	img = imread(im_path)
	img_h = img.shape[0]
	img_w = img.shape[1]

	#max_size = 350
	#max_size = 300
	
	max_dim = max(img_h, img_w)

	if max_dim>max_size:
		ratio = float(max_dim)/float(max_size)
		ratio = int(100.0/ratio)
		#cmd = 'mogrify -resize 50% ' + im_path
		cmd = 'mogrify -resize ' + str(ratio) +  '% ' + im_path
		os.system(cmd)

	return im_path

def segment_image(im_path,image_url,image_data):
	#im_path = os.path.join(os.getcwd(),'image.jpg')
	#img = Image.open(im_path)
	#img_w, img_h = img.size

	img = imread(im_path)
	img_h = img.shape[0]
	img_w = img.shape[1]
		
	#s_tuple = net.blobs['data'].data.shape
	s_tuple = (1, 3, img_h, img_w)

	#transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
	transformer = caffe.io.Transformer({'data': s_tuple})
	transformer.set_mean('data', np.load(os.path.join(os.getcwd(),'model','ilsvrc_2012_mean.npy')).mean(1).mean(1))
	transformer.set_transpose('data', (2,0,1))
	transformer.set_channel_swap('data', (2,1,0))
	transformer.set_raw_scale('data', 255.0)

	net.blobs['data'].reshape(1,s_tuple[1],s_tuple[2],s_tuple[3])

	im = caffe.io.load_image(im_path)
	net.blobs['data'].data[...] = transformer.preprocess('data', im)
	out = net.forward()
	probs = net.blobs['fc8_interp'].data
	probs = np.squeeze(probs)
	labels = np.argmax(probs,axis=0)
	labels = labels[:img_h,:img_w]

	image_attributes = extract_colors(im_path,color_lab_matrix_path,color_names_path,labels,False)

	#image_data = {}
	image_data['height'] = image_attributes['height']
	image_data['width'] = image_attributes['width']
	#image_data['url'] = image_url
	image_data['items'] = ''
	#image_data['name'] = 'placeholder.jpg'
		
	desc_str = ','
	desc_color_str = ','
	image_data['info'] = {}
	for k in image_attributes['info'].keys():
		image_data['info'][k.lower()] = image_attributes['info'][k]
		
		if k in description_labels:
			desc_str = desc_str + k.lower() +', '
			desc_color_str = desc_color_str + image_data['info'][k.lower()]['color'] + ' ' + k.lower() +', '

	desc_str = desc_str.strip()
	desc_str = desc_str.strip(',')
	image_data['items'] = desc_str

	desc_color_str = desc_color_str.strip()
	desc_color_str = desc_color_str.strip(',')
	image_data['items_with_color'] = desc_color_str

	return image_data
	#json_str = json.loads(json.dumps(image_data))
	#print(json.dumps(json_str, indent=4, sort_keys=True))

def main():
	image_url = sys.argv[1]
	im_path = download_image(image_url)
	segment_image(im_path,image_url)
	
if __name__ == '__main__':
	main()
