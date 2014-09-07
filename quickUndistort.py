
import sys
import numpy as np
import cv2

file_name = sys.argv[1] or file_name
img = cv2.imread(file_name)
(h,w) = img.shape[:2]

#ret, mtx, dist, rvecs, tvecs
#current calibration to test
camera_matrix = np.eye(3)
camera_matrix[0][0] = 1.76229007e+03
camera_matrix[1][1] = 1.76399667e+03
camera_matrix[0][2] = 1.98223642e+03
camera_matrix[1][2] = 1.48604382e+03

#dist_coefs = np.array([-0.26063938, 0.10406917, -0.00084988, 0,0])
#dist_coefs = np.array([-0.26063938, 0.10406917, -0.00084988, -0.00046085, 0])
dist_coefs = np.array([-0.26063938, 0.10406917, -0.00084988, -0.00046085, -0.0251081])

new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix,dist_coefs,(w,h),1,(w,h))



#undistort
# undistort
dst = cv2.undistort(img, camera_matrix, dist_coefs, None, new_camera_matrix)
cv2.imwrite('calibresultfull.png',dst)

# crop the image
x,y,w,h = roi
dst = dst[y:y+h, x:x+w]
cv2.imwrite('calibresult.png',dst)


