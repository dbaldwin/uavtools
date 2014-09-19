
import sys
import os

import numpy as np
import cv2

from calibration.utils import read_calibration_file

def undistort_image(fname, camera_matrix, dist_coefs, fname_out='', crop=False):
	if not fname_out:
		sp = os.path.split(fname)
		fname_out = os.path.join(sp[0],'undistorted_'+sp[1])

	img = cv2.imread(fname)	
	(h,w) = img.shape[:2]

	new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix,dist_coefs,(w,h),1,(w,h))
	
	dst = cv2.undistort(img, camera_matrix, dist_coefs, None, new_camera_matrix)
	if crop:# crop the image
		x,y,w,h = roi
		dst = dst[y:y+h, x:x+w]

	cv2.imwrite(fname_out,dst)


if __name__ == '__main__':
	cal_fname = sys.argv[1]
	img_fname = sys.argv[2]
	camera_matrix, dist_coefs = read_calibration_file(cal_fname)

	undistort_image(img_fname,camera_matrix,dist_coefs)


