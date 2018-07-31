def label_merging(labels_flat, category_labels):
	input_label = [['UpperClothes','Skirt','Pants'],['RightShoe'],['RightLeg'],['RightArm']]
	target_label = ['Dress','LeftShoe','LeftLeg','LeftArm']

	for count, tgl in enumerate(target_label):
		tgl_idx = category_labels.index(tgl)

		for inp_count,inp_label in enumerate(input_label[count]):
			inp_idx = category_labels.index(inp_label)
			labels_flat[labels_flat == inp_idx] = tgl_idx

	return labels_flat
