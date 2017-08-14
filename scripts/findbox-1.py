import numpy as np
from pyimagesearch.shapedetector import ShapeDetector
from pyimagesearch.canny import auto_canny
import save
import moments
import imutils
import os
import cv2
from pprint import pprint
# import random
import argparse

contourColors = [
	[255,0,0],
	[0,255,0],
	[0,0,255],
	[0,255,255],
	[255,0,255],
	[255,255,0],
	[255,125,0],
	[255,125,125],
	[125,255,0],
	[125,255,125],
	[0,125,255],
	[125,125,255],
	[125,255,255],
	[255,125,255],
	[255,255,125],
]

def main(srcFile, outDir):
	filename = os.path.basename(srcFile)
	fileOutDir = os.path.join(outDir, filename)
	if not os.path.exists(fileOutDir):
		os.makedirs(fileOutDir)

	src = cv2.imread(srcFile)
	save.src(fileOutDir, filename, src)

	dst = src.copy()
	img = src.copy()

	img = imutils.resize(img, width=300)

	img = cv2.dilate(img, None, iterations=4)
	img = cv2.erode(img, None, iterations=4)

	img = cv2.bilateralFilter(img,20,75,75)
	save.int(fileOutDir, filename, "bilateral", img)

	# kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
	# img = cv2.filter2D(img, -1, kernel)
	# save.int(fileOutDir, filename, "sharp", img)

	# img = cv2.Canny(img, 30, 200)
	img = auto_canny(img, 0.8)
	# img = cv2.dilate(img, None, iterations=3)
	# img = cv2.erode(img, None, iterations=2)
	save.int(fileOutDir, filename, "canny", img)

	cnts = moments.findApprox(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnts = moments.inApproxEdgeRange(cnts, 3, 7)
	cnts = moments.inAreaRange(src, cnts, .6, .95)
	i = 0
	for c in cnts:
		contour = c["Contour"]
		moments.drawContour(dst, img, contour, contourColors[i])
		i = i + 1
		moments.drawApproxPoints(dst, img, contour, contourColors[i])
		i = i + 1

	save.dst(fileOutDir, filename, dst)
	return

parser = argparse.ArgumentParser()
# parser.add_argument("--verbosity", help="increase output verbosity")
parser.add_argument("--src", help="src directory")
parser.add_argument("--out", help="out directory")
args = parser.parse_args()

files = []
for f in os.listdir(args.src):
	f = args.src+"/"+f
	if os.path.isfile(f) and f.lower().endswith(('.png', '.jpg', '.jpeg')):
		main(f, args.out)
