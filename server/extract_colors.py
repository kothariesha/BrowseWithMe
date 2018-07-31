import numpy as np
from scipy.misc import imread
from colorextractor import ColorExtractor
#from label_merging import *
import cPickle as pickle
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff_matrix import delta_e_cie2000

category_original_labels = ['background',    'Hat',    'Hair',    'Sunglasses',    'Top',    'Skirt',    'Pants',    'Dress',    'Belt',    'LeftShoe',    'RightShoe', 'Face' ,   'LeftLeg',    'RightLeg',    'LeftArm',    'RightArm',    'Bag',    'Scarf'];

category_merged_labels = ['background',    'Hat',    'Hair',    'Sunglasses',    'Top',    'Skirt',    'Pants',    'Dress',    'Belt',    'Shoe',    'RightShoe', 'Face' ,   'Leg',    'RightLeg',    'Arm',    'RightArm',    'Bag',    'Scarf'];

		
def extract_colors(img_path,color_lab_matrix_path,color_names_path,labels,merge_labels):
	quality=1
	
	lab_matrix = pickle.load(open(color_lab_matrix_path,'rb'))
	color_names = pickle.load(open(color_names_path,'rb'))

	img = imread(img_path)
	num_rows = img.shape[0]
	num_cols = img.shape[1]
	num_pixels = num_rows*num_cols 
		
	ce = ColorExtractor()
	image_attributes = {}
	image_attributes['height'] = num_rows
	image_attributes['width']  = num_cols
	#image_attributes['name'] = im_prefix +  ext
	category_labels = category_original_labels

	img_flat = img.transpose(2,0,1).reshape(3,-1).T

	if merge_labels == True:
		labels = label_merging(labels, category_labels)
		category_labels = category_merged_labels

	labels_flat = np.ravel(labels)
		
	uniq_labels = np.unique(labels_flat)	
	color_pallete = {}

	for ind in list(uniq_labels):
		img_region = img_flat[labels_flat == ind]
		pixel_list = list(tuple(map(tuple,img_region)))	
		num_colors = 5
		
		labels_region = (labels == ind)
		ymax, xmax = np.max(np.where(labels_region == True), 1)
		ymin, xmin = np.min(np.where(labels_region == True), 1)
		region_box = [xmin, ymin, xmax, ymax]
		
		pallete = ce.get_palette(pixel_list, color_count=num_colors,quality=quality)
	
		pallete = pallete[0]
		pixel_area = round((100.0*img_region.shape[0])/num_pixels,2)
		
		if pixel_area<1:
			continue

		r = pallete['r']/255.0
		g = pallete['g']/255.0
		b = pallete['b']/255.0
		
		color_rgb = sRGBColor(r, g, b);
		color_lab = convert_color(color_rgb, LabColor);
		color_lab_vec = np.array([color_lab.lab_l, color_lab.lab_a, color_lab.lab_b])
		delta = delta_e_cie2000(color_lab_vec, lab_matrix)
		color_name = color_names[np.argmin(delta)]

		rgb_values = {}
		rgb_values['r'] = pallete['r']
		rgb_values['g'] = pallete['g']
		rgb_values['b'] = pallete['b']

		color_pallete[category_labels[ind]] = {'color':color_name, 'pixel_area':pixel_area, 'box':region_box, 'rgb':rgb_values}

	image_attributes['info'] = color_pallete
	return image_attributes
