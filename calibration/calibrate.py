import sys
import os

import numpy as np
import cv2

from calibration.utils import write_calibration_file

def calibrate(image_names, pattern_size=(8,6), debug=False, calibration_file_name='default_calibration.json'):

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
		(h,w) = img_gray.shape

		ret, corners = cv2.findChessboardCorners(img_gray, pattern_size ,None)

		#if board is found
		if ret == True:
			print 'Checkerboard found in image: ' + fname

			#refine corners to increase accuracy
			cv2.cornerSubPix(img_gray,corners,(11,11),(-1,-1),criteria)

			#storing grid location data
			img_points.append(corners.reshape(-1,2))
			obj_points.append(pattern_points)

			print debug

			if debug:
				rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, (w, h), None, None)
				print 'intermediate results:'
				print 'RMS:', rms
				print 'camera matrix:\n', camera_matrix
				print 'distortion coefficients: ', dist_coefs.ravel()

				sp = os.path.split(fname)
				debug_fname = sp[0] + '\debug_out_' + sp[1]
				print 'writing debug image to: ' + debug_fname
				cv2.drawChessboardCorners(img, pattern_size, corners, ret)
				cv2.imwrite(debug_fname, img)
		else:
			print 'Checkerboard not found in image: ' + fname

		count += 1

	#final output
	print 'final calculated camera matrix:'
	rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, (w, h), None, None)
	print 'RMS:', rms
	print 'camera matrix:\n', camera_matrix
	print 'distortion coefficients: ', dist_coefs.ravel()

	print 'writing to file: ' + calibration_file_name
	write_calibration_file(camera_matrix,dist_coefs,calibration_file_name)


if __name__ == '__main__':
	calibrate(image_names=sys.argv[1:],debug=True)

