## Overview

This codebase allows you to run the server side code for BrowseWithMe system

1) Download the deep learning model file from the following link and store it inside the models directory.
	- [Download](https://drive.google.com/file/d/1X16N0FVMawUnKw64N5QDTgCBVlTVzBp8/view?usp=sharing)

2) Dependencies: 
	- Download and install Deeplab-v2 from [here](https://bitbucket.org/aquariusjay/deeplab-public-ver2)
	- Set the caffe binary path (caffe_root) in fashion_parsing.py correctly.

3) Running the server: Open a terminal window and use the following command:
```
python BrowseWithMeVision.py
```

4) Testing on a client: Open another terminal window on the same host and use the following command:

```
sh run_server.sh <image_url> 

Example:
sh run_server.sh "http://www.sophiecliff.com/wp-content/uploads/2015/10/asos-glitter-star-flutter-sleeve-maxi-dress.jpg"
```
