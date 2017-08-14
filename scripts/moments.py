
import imutils
from imutils import perspective
import cv2
from pprint import pprint

def findContours(img, a, b):
	ret = []
	cnts = cv2.findContours(img, a, b)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	for c in cnts:
		M = cv2.moments(c)
		if M["m00"] > 0:
			ret.append({"Moment":M, "Contour":c})
	return ret

def findApprox(img, a, b, delta=0.02):
	ret = []
	cnts = cv2.findContours(img, a, b)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	for c in findContours(img, a, b):
		epsilon = delta*cv2.arcLength(c["Contour"], True)
		approx = cv2.approxPolyDP(c["Contour"], epsilon, True)
		c["Approx"] = approx
		ret.append(c)

	return ret

def inAreaRange(srcImg, contours, min, max):
	ret = []
	for c in contours:
		x,y,w,h = cv2.boundingRect(c["Contour"])
		r = h / float(srcImg.shape[0])
		if min<r<max:
			ret.append(c)
	return ret

def inApproxEdgeRange(contours, min, max):
	ret = []
	for c in contours:
		if min<len(c["Approx"])<max:
			ret.append(c)
	return ret

def inEdgeRange(contours, min, max):
	ret = []
	for c in contours:
		if min<len(c["Contour"])<max:
			ret.append(c)
	return ret

def drawContour(dstImg, srcImg, contour, color):
	ratio = dstImg.shape[0] / float(srcImg.shape[0])

	contour = contour.astype("float")
	contour *= ratio
	contour = contour.astype("int")

	cv2.drawContours(dstImg, [contour], -1, color, 2)
	return

def drawApprox(dstImg, srcImg, contour, color, epsilon=0.02):
	epsilon = 0.02*cv2.arcLength(contour, True)
	approx = cv2.approxPolyDP(contour, epsilon, True)

	return drawContour(dstImg, srcImg, approx, color)

def drawContourPoints(dstImg, srcImg, contour, color):
	ratio = dstImg.shape[0] / float(srcImg.shape[0])

	contour = contour.astype("float")
	contour *= ratio
	contour = contour.astype("int")

	for p in contour:
		(x, y) = p[0]
		cv2.circle(dstImg, (int(x), int(y)), 5, color, -1)
	return

def drawApproxPoints(dstImg, srcImg, contour, color, epsilon=0.02):
	epsilon = 0.02*cv2.arcLength(contour, True)
	approx = cv2.approxPolyDP(contour, epsilon, True)

	return drawContourPoints(dstImg, srcImg, approx, color)

def isProbablyARectangle(contour, deviation=60):
	# see also extreme points of a contour
	# box = perspective.order_points(box)
	return
