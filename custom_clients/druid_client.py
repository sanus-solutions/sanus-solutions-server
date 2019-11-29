import requests, json, datetime
## configuration import 

class DruidClient():

	def __init__(self, ):
		## Temporary local variables, will move to configuration file soon
		self.url = "http://192.168.0.101:8200/v1/post/daycare"
		self.headers = {"Content_Type" : "application/json"}

	def inject(self, node_id, staff_id, timestamp):
		timestamp = datetime.datetime.utcfromtimestamp(timestamp).isoformat()
		payload = {
			'time' : timestamp,
			'type' : None,
			'node_id' : node_id,
			'staff_id' : staff_id,
			'staff_title' : None,
			'unit' : None,
			'room_number' : None,
			'response_type' : None,
			'response_message' : None,
		} 
		result = requests.post(self.url, json = payload, headers=self.headers)

		return result

if __name__ == '__main__':
	import time
	client = DruidClient()
	client.inject(1,2,time.time())