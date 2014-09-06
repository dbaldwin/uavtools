import sys

import numpy as np
import cv2

def main():
	image_names =  sys.argv[1:]
	pattern_size = (8,6)

	if not image_names:
		print
		print 'No calibration images supplied'
		print 'Usage:'
		print '\tpython calibrate.py [file2 file2 file3 ...]'
		print
		return;

	# termination criteria
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

	# holding the calibration data points as they are collected
	obj_points = [] # 3d point in real world space
	img_points = [] # 2d points in image 

	#array of points representing the calibration image location in 3D space
	#  this is appended to obj_points everytime the grid is located in an image
	pattern_points = np.zeros( (np.prod(pattern_size), 3), np.float32 )
	pattern_points[:,:2] = np.indices(pattern_size).T.reshape(-1, 2)

	count = 0
	for fname in image_names:
		print 'testing file: ' + fname + ': ' + str(count) + ' of ' + str(len(image_names))
		img = cv2.imread(fname)
		img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

		ret, corners = cv2.findChessboardCorners(img_gray, pattern_size ,None)

		#if board is found
		if ret == True:
			print 'Checkerboard found in image: ' + fname

			#refine corners to increase accuracy
			cv2.cornerSubPix(img_gray,corners,(11,11),(-1,-1),criteria)

	        # Draw and display the corners
			#cv2.drawChessboardCorners(img, pattern_size, corners, ret)
			#img_small = cv2.resize(img,(800,600), interpolation=cv2.INTER_LINEAR)
	    
			#storing grid location data
			img_points.append(corners.reshape(-1,2))
			obj_points.append(pattern_points)

			#cv2.namedWindow('img')
			#cv2.imshow('img',img_small)
			#cv2.waitKey(500)
		else:
			print 'Checkerboard not found in image: ' + fname

		count += 1

	cv2.destroyAllWindows()

	rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, (w, h), None, None)
	print "RMS:", rms
	print "camera matrix:\n", camera_matrix
	print "distortion coefficients: ", dist_coefs.ravel()


if __name__ == '__main__':
	main()

