import sys
import rawpy
import time
import cv2

start = time.time()

if len(sys.argv) > 2:
	print("One image at a time, please.")
elif len(sys.argv) == 1:
	print("Please provide an image.")

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
grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Histogram equalization: https://docs.opencv.org/2.4/doc/tutorials/imgproc/histograms/histogram_equalization/histogram_equalization.html
# Or if the image is dark, don't equalize histogram? So no seriousbanding or noise is introduced.
equalized_grayscale = cv2.equalizeHist(grayscale)
# Histogram equalization means noise is introduced.
denoised = cv2.fastNlMeansDenoising(equalized_grayscale, 10, 21, 7)
cv2.imwrite("test.jpg", grayscale)
cv2.imwrite("test_eq.jpg", equalized_grayscale)
cv2.imwrite("test_eq_denoised.jpg", denoised)
# Variance of Laplacian is a measure of focus
var_lap = cv2.Laplacian(grayscale, cv2.CV_64F).var()
var_lap_eq = cv2.Laplacian(equalized_grayscale, cv2.CV_64F).var()
var_lap_eq_denoised = cv2.Laplacian(denoised, cv2.CV_64F).var()
print("Score with Laplacian: " + str(var_lap))
print("Score with equalized histogram: " + str(var_lap_eq))
print("Score with denoising: " + str(var_lap_eq_denoised))
end = time.time()
print("Time elapsed: " + str(end - start))
