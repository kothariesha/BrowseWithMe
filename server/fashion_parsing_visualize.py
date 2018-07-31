import numpy as np
from label_merging import *
from scipy.misc import imread
from scipy.io import loadmat

category_original_labels = ['Background',    'Hat',    'Hair',    'Sunglasses',    'UpperClothes',    'Skirt',    'Pants',    'Dress',    'Belt',    'LeftShoe',    'RightShoe', 'Face' ,   'LeftLeg',    'RightLeg',    'LeftArm',    'RightArm',    'Bag',    'Scarf'];

category_merged_labels = ['Background',    'Hat',    'Hair',    'Sunglasses',    'UpperClothes',    'Skirt',    'Pants',    'Dress',    'Belt',    'Shoe',    'RightShoe', 'Face' ,   'Leg',    'RightLeg',    'Arm',    'RightArm',    'Bag',    'Scarf'];

def visualize(img_path,labels,merge_labels, colormap_file):
	#cmap_pascal = loadmat('pascal_seg_colormap.mat')
	
	cmap_pascal = loadmat(colormap_file)
	cmap_pascal = cmap_pascal['colormap']
	
	img = imread(img_path)
	num_rows = img.shape[0]
	num_cols = img.shape[1]
	num_pixels = num_rows*num_cols 

	category_labels = category_original_labels

	if merge_labels == True:
		labels = label_merging(labels, category_labels)
		category_labels = category_merged_labels

				
	labels_rgb_img = cmap_pascal[labels]; 
	labels_rgb_img_uint = (labels_rgb_img * 255).round().astype(np.uint8)

	viz_img = np.concatenate((img,labels_rgb_img_uint),axis=1);
	"""
	if merge_labels == True:
		colormap_img = imread('colormaps_merged.png')
	else:
		colormap_img = imread('colormaps.png')

	colormap_img = imresize(colormap_img,(viz_img.shape[0],colormap_img.shape[1]))
	colormap_img = colormap_img[:,:,:3]

	viz_img = np.concatenate((viz_img,colormap_img),axis=1)
	"""

	return viz_img
