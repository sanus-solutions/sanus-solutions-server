from __future__ import print_function
import sys, os, requests, time, json
import base64, dlib#, cv2
import numpy as np


class PCClient:
	"""
	Test client class for pc/laptop with webcam
	"""
	def __init__(self, ctype, node_id):
		# self.cap = cv2.VideoCapture(0)
		self.image = None
		self.ctype = ctype
		self.node_id = node_id

		if self.ctype == 'san':
			self.url = 'http://localhost:5000/sanushost/api/v1.0/sanitizer_img'
		elif self.ctype == 'ent':
			self.url = 'http://localhost:5000/sanushost/api/v1.0/entry_img'

	def capture_and_post(self, image=None):
		timestamp = time.time()
		try:
			image.shape
			img = image
		except:
			_, img = self.cap.read()
		shape = str(img.shape)
		img = img.astype(np.float64)
		image_64_str = base64.b64encode(img)
		payload = {'NodeID': self.node_id, 'Timestamp': timestamp, 'Image': image_64_str, 'Shape': shape}
		headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
		result = requests.post(self.url, json=payload, headers=headers)
		print(result)




if __name__ == '__main__':
	client = PCClient('san', 'first')
	image = dlib.load_rgb_image('/Users/billyzheng/face_test/wjx_test_far_extreme.jpg')
	client.capture_and_post(image)













