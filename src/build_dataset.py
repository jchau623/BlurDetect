## Takes in a folder path and reads all the images through read_raw.py

import sys
import os
import read_raw
import rawpy
import numpy as np
import cv2

### FUNCTION DEFS
## Credits to: https://ssscripting.wordpress.com/2009/03/03/python-recursive-directory-walker/
def processAndScoreImage(path):
	# Check if file is an image and can be processed or not
	img = None
	try:
		img = rawpy.imread(path)
		img = img.postprocess()
	except:
		try:
			img = cv2.imread(path)
		except:
			return None
	processed = read_raw.processImage(img)
	scores = read_raw.obtainScores(img)
	return list(scores.values())

def populate_DS(dir,dst, meth):
	""" walks a directory, and executes a callback on each file """
	dir = os.path.abspath(dir)
	for file in [file for file in os.listdir(dir) if not file in [".",".."]]:
		nfile = os.path.join(dir,file)
		scores = meth(nfile)
		if scores != None:
			dst.append(scores)
		if os.path.isdir(nfile):
			processAndScoreImage(nfile,meth)

#label = 0 if blurry, 1 if sharp
def build(path, label):
	DS_X = []
	populate_DS(path, DS_X, processAndScoreImage)
	NPDS_X = np.array(DS_X)
	NPDS_Y = None
	if label == 0:
		NPDS_Y = np.zeros(NPDS_X.shape[0])
	elif label == 1:
		NPDS_Y = np.ones(NPDS_X.shape[0])
	try:
		X_file = np.load("../training_np_arrays/X.npy")
		X_file = np.append(X_file, NPDS_X, axis=0)
	except:
		X_file = NPDS_X
	np.save("../training_np_arrays/X.npy", X_file)
	try:
		Y_file = np.load("../training_np_arrays/Y.npy")
		Y_file = np.append(Y_file, NPDS_Y, axis=0)
	except:
		Y_file = NPDS_Y
	np.save("../training_np_arrays/Y.npy", Y_file)

def reset_saved_NPY(path):
	#TODO
	pass
###