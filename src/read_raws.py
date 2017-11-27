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

def laplacianVariance(image):
	return cv2.Laplacian(image, cv2.CV_64F).var()

def modifiedLaplacian(image):
	M = np.array([[-1.], [2.], [-1.]])
	G = cv2.getGaussianKernel(3, -1, cv2.CV_64F)
	Lx = cv2.sepFilter2D(image, -1, M, G)
	Ly = cv2.sepFilter2D(image, -1, G, M)
	FM = np.abs(Lx) + np.abs(Ly)
	return cv2.mean(FM)[0]

def tenengrad(image, ksize):
	Gx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize)
	Gy = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize)
	FM = np.square(Gx) + np.square(Gy)
	return cv2.mean(FM)[0]

def GLVN(image):
	m = cv2.meanStdDev(image)
	mu = m[0][0]
	sigma = m[1][0]
	return (sigma[0] * sigma[0]) / mu[0]
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
denoised = applyDenoising(equalized_grayscale, 10, 7, 21)
cv2.imwrite("test.jpg", grayscale)
cv2.imwrite("test_eq.jpg", equalized_grayscale)
cv2.imwrite("test_eq_denoised.jpg", denoised)
# Variance of Laplacian is a measure of focus
var = laplacianVariance(img)
var_lap = laplacianVariance(grayscale)
var_lap_eq = laplacianVariance(equalized_grayscale)
var_lap_eq_denoised = laplacianVariance(denoised)
print("Score: " + str(var))
print("Score with grayscale: " + str(var_lap))
print("Score with equalized histogram: " + str(var_lap_eq))
print("Score with denoising: " + str(var_lap_eq_denoised))
modified_lap = modifiedLaplacian(denoised)
print("modifiedLaplacian: " + str(modified_lap))
tenengrad_score = tenengrad(denoised, 7)
print("Tenengrad: " + str(tenengrad_score))
glvn_score = GLVN(denoised)
print("GLVN: " + str(glvn_score))
end = time.time()
print("Time elapsed: " + str(end - start) + "\n")