## Overview

This codebase allows you to run the server side code for BrowseWithMe system.

If you use this in your research, please cite the following papers:

```sh
@article{browsewithme,
	Author = {A. J. Stangl, E. Kothari, S. D. Jain, T. Yeh, K. Grauman, and D. Gurari},
	Title = {BrowseWithMe: Design and Prototype of an Online Clothes Shopping Assistant for People with Visual Impairments},
	Journal = {ACM SIGACCESS Conference on Computers and Accessibility (ASSETS)},
	Year = {2018}
}
```

## Instructions:

1) Download the deep learning model file from the following link and store it inside the "model" directory.
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

5) Note that BrowseWithMe.py contains the code for complete system (including NLP), however the website tags change frequently hence the NLP codebase needs to be updated for running sucessfully. 


