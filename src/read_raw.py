import sys
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

def obtainScores(image):
	scores = {}
	scores["LAPV"] = laplacianVariance(image)
	scores["LAPM"] = laplacianVariance(image)
	scores["TENG"] = tenengrad(image, 7)
	scores["GLVN"] = GLVN(image)
	return scores

def processImage(image):
	# downsize the image for speed performance
	img = resizeToMax1000Shape(image)
	grayscale = convertToGrayscale(img)
	# Adjust brightness
	grayscale = adjust_gamma(grayscale, 3)
	equalized_grayscale = applyCLAHE(3.0, (10,10), grayscale)
	# Histogram equalization means noise is introduced.
	denoised = applyDenoising(equalized_grayscale, 10, 7, 21)
	return denoised
###