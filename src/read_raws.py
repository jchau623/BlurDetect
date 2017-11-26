import sys
import rawpy
import time
import cv2
import numpy as np

### Function definitions
def resizeToMax1000Shape(image):
	shape = image.shape;
	if shape[0] > shape[1]:
		high = shape[0]
	else:
		high = shape[1]
	if high < 1000:
		return image
	else:
		factor = 1000/high
		downsized = cv2.resize(image, (0,0), fx=factor, fy=factor)
		return downsized

# https://docs.opencv.org/3.1.0/d5/daf/tutorial_py_histogram_equalization.html
def applyCLAHE(cl, tgs, image):
	return cv2.createCLAHE(clipLimit=cl, tileGridSize=tgs).apply(image)

# https://docs.opencv.org/3.0-beta/modules/photo/doc/denoising.html#fastnlmeansdenoising
def applyDenoising(img, h, templateWindowSize, searchWindowSize):
	return cv2.fastNlMeansDenoising(img, h, templateWindowSize, searchWindowSize)

def convertToGrayscale(img):
	return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Taken from https://www.pyimagesearch.com/2015/10/05/opencv-gamma-correction/
# Credit to pyimagesearch
# gamma > 1 = brighter
def adjust_gamma(image, gamma):
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
 
	# apply gamma correction using the lookup table
	return cv2.LUT(image, table)
###

start = time.time()

if len(sys.argv) > 2:
	print("One image at a time, please.")
	exit()
elif len(sys.argv) == 1:
	print("Please provide an image.")
	exit()

path = sys.argv[1]
try:
	img = rawpy.imread(path)
	img = img.postprocess()
except:
	try:
		img = cv2.imread(path)
	except:
		exit()

if img is None:
	exit()
else:
	print(path)

#grayscale = (0.21*img[:,:,0])+(0.72*img[:,:,0])+(0.07*img[:,:,0])
# downsize the image for speed performance
img = resizeToMax1000Shape(img)
grayscale = convertToGrayscale(img)
# Adjust brightness
grayscale = adjust_gamma(grayscale, 3)
equalized_grayscale = applyCLAHE(3.0, (10,10), grayscale)
# Histogram equalization means noise is introduced.
denoised = applyDenoising(equalized_grayscale, 10, 21, 7)
cv2.imwrite("test.jpg", grayscale)
cv2.imwrite("test_eq.jpg", equalized_grayscale)
cv2.imwrite("test_eq_denoised.jpg", denoised)
# Variance of Laplacian is a measure of focus
var = cv2.Laplacian(img, cv2.CV_64F).var()
var_lap = cv2.Laplacian(grayscale, cv2.CV_64F).var()
var_lap_eq = cv2.Laplacian(equalized_grayscale, cv2.CV_64F).var()
var_lap_eq_denoised = cv2.Laplacian(denoised, cv2.CV_64F).var()
print("Score: " + str(var))
print("Score with grayscale: " + str(var_lap))
print("Score with equalized histogram: " + str(var_lap_eq))
print("Score with denoising: " + str(var_lap_eq_denoised))
print("Score: " + str(var))
end = time.time()
print("Time elapsed: " + str(end - start) + "\n")