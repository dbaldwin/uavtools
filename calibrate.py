import sys

import numpy as np
import cv2

def main():
	image_names =  sys.argv[1:]
	if not image_names:
		print
		print 'No calibration images supplied'
		print 'Usage:'
		print '\tpython calibrate.py [file2 file2 file3 ...]'
		print
		return;

	# termination criteria
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

	# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
	objp = np.zeros((6*7,3), np.float32)
	objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

	# Arrays to store object points and image points from all the images.
	objpoints = [] # 3d point in real world space
	imgpoints = [] # 2d points in image plane.

	count = 0
	for fname in image_names:
		print 'testing file: ' + fname + ': ' + str(count) + ' of ' + str(len(image_names))
		img = cv2.imread(fname)
		gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	    # Find the chess board corners
		ret, corners = cv2.findChessboardCorners(gray, (9,7),None)

	    # If found, add object points, image points (after refining them)
		if ret == True:
			print 'Checkerboard found in image: ' + fname
			objpoints.append(objp)

			corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
			imgpoints.append(corners2)

	        # Draw and display the corners
			img = cv2.drawChessboardCorners(img, (7,6), corners2,ret)
			cv2.imshow('img',img)
			cv2.waitKey(500)
		else:
			print 'Checkerboard not found in image: ' + fname

		count += 1

	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()

