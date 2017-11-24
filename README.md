# BlurDetect
A lightroom plugin that lets you discard all blurry photos from catalogue during import

## Keywords
Computer vision, Lightroom, plugin, extension, python, Lua

# Links, Resources:

* Blur detection: https://www.pyimagesearch.com/2015/09/07/blur-detection-with-opencv/
* Good discussion: https://stackoverflow.com/questions/7765810/is-there-a-way-to-detect-if-an-image-is-blurry
* Fourier transform: 
  * https://betterexplained.com/articles/an-interactive-guide-to-the-fourier-transform/
  * https://math.stackexchange.com/questions/1002/fourier-transform-for-dummies
* Paper, *Analysis of focus measure operators for shape-from-focus* : https://pdfs.semanticscholar.org/8c67/5bf5b542b98bf81dcf70bd869ab52ab8aae9.pdf
  * If have time and energy, try using a focus detect with lower average computation time (Table 5)
* http://www.cse.cuhk.edu.hk/leojia/all_final_papers/blur_detect_cvpr08.pdf
* Saliency detection (only select the area of the picture that "stands out," or is "salient." This way pictures with small subjects and large bokeh backgrounds won't flag as false positives.): 
  * https://blog.algorithmia.com/introduction-image-saliency-detection/
  * https://docs.opencv.org/3.0-beta/modules/saliency/doc/saliency.html
* "Laplacian edge detection": http://www.owlnet.rice.edu/~elec539/Projects97/morphjrks/laplacian.html
* Image normalization:
  * Histogram stretching:  
    * http://effbot.org/zone/pil-histogram-equalization.htm
 * Normalizing brightness: https://stackoverflow.com/a/38138050
* Using RAW images in numpy: https://pypi.python.org/pypi/rawpy
* Some code for converting matrix of image to black and white: https://imagepy.wordpress.com/2015/11/21/raw-image-processing-in-python-an-example/

# Plan
1. Convert images to grayscale
2. Calculate variance of Laplacian (a measure of sharpness/blurriness)
3. The images that fail to meet a threshold (the example sets it at 100) are "blurry"
4. **(Requires a Windows machine)** Use [Lightroom SDK](https://www.adobe.io/apis/creativecloud/lightroom.html) to develop a plugin
    1. On import runs all photos through the algorithm
    2. Opens a new dialog box with all images that fail to meet the thredhold
        1. If RAW images, use show embedded JPEG preview
    3. Removes all selected images from dialog box from catalogue
5. Improve filtering by:
    1. Image normalization (normalize contrast and brightness)
    2. Saliency detection
