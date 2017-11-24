import sys
import rawpy
import cv2

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
		pass

#grayscale = (0.21*img[:,:,0])+(0.72*img[:,:,0])+(0.07*img[:,:,0])
grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(grayscale)
# Variance of Laplacian is a measure of focus
var_lap = cv2.Laplacian(img, cv2.CV_64F).var()
print(var_lap)