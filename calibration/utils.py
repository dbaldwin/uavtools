
import json

import numpy as np

def write_calibration_file(cam_matrix,distortion,filename='default_calibration.json'):
	with open(filename,'w') as f:
		data = {}	
		data['distortion'] = distortion.tolist()
		data['camera_matrix'] = {'shape':cam_matrix.shape, 'elements':cam_matrix.tolist()}

	 	f.write(json.dumps(data))

def read_calibration_file(filename='default_calibration.json'):
	with open(filename,'r') as f:
		data = json.loads(f.read())

	if not data:
		#exception
		return

	distortion = np.array(data['distortion'])	
	camera_matrix = np.array(data['camera_matrix']['elements'])

	return camera_matrix, distortion
