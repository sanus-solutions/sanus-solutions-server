import numpy as np
import time
from sanus_face_server.custom_clients import demo_util

"""
minimal implementation of graph structure
"""
class SimpleGraph():
	"""
	underlying data structure saved in self.node_list
	node_list is a dictionary with node_id as key and info of node as value
	node info is a dictionary with neighbors, node type, latest embeddings, and latest timestamp
	"""
	def __init__(self):
		self.node_list = {}
		self.time_thresh = 100 # seconds
		self.dist_thresh = 0.15 # TODO: what's a good similarity threshold here????

	"""loss metrics"""
	def cosine_similarity(self, emb1, emb2):
		return np.dot(emb1, emb2)/(np.sqrt(np.sum(np.square(emb1))*np.sum(np.square(emb2))))

	def euclidean_distance(self, emb1, emb2):
		return 1 - np.sqrt(np.sum(np.square(emb1 - emb2)))

	"""graph utilities"""
	def get_graph(self):
		print(self.node_list)
		return self.node_list

	def update_neighbors(self, node_id, neighbors):
		for neighbor in neighbors:
			self.node_list[neighbor]['Neighbors'].append(node_id)

	def update_node(self, embeddings, timestamp, node_id):
		try:
			self.node_list[node_id]['embeddings'] = embeddings
			self.node_list[node_id]['timestamp'] = timestamp
			return 1
		except KeyError:
			print('node does not exist in the graph.')
			return 0

	def check_breach(self, embeddings, timestamp, node_id):
		"""
		return 1 if breach detected, 0 if no breach detected, and 'fail' if check failed
		this only happens at an entry node
		# TODO: how many layers of neighbors do we check??? this is for later
			    right now just neighbors
		"""
		try:
			node = self.node_list[node_id]
		except KeyError:
			print('Node does not exist in the graph.')
			return 'Fail'
		neighbors = node['neighbors']
		for neighbor in neighbors:
			neighbor_node = self.node_list[neighbor]
			# TODO: are there situations where we need to check neighboring entry nodes?
			if neighbor_node['node_type'] == 'san':
				latest_embeddings = neighbor_node['embeddings']
				dist = self.euclidean_distance(latest_embeddings, embeddings)
				time_elapsed = abs(timestamp - neighbor_node['timestamp']) # technically don't need abs here but just in case
				if time_elapsed < self.time_thresh and dist < self.dist_thresh:
					return 0
				else:
					return 1
		return 1

	def add_node(self, node_id, neighbors, node_type, embeddings=None, timestamp=None):
		"""
		node_id should be a string
		neighbors should be list of node_id strings
		node_type should be a string
		embeddings and timestamp default to None
		"""
		try:
			temp = self.node_list[node_id]
			print('Node exists, with neighbors: ' + str(temp['neighbors']) + 'and type ' + temp['node_type'])
			return 0
		except KeyError:
			print('Adding node now.')
			self.node_list[node_id] = {'neighbors': neighbors, 'node_type': node_type, 'embeddings': embeddings, 'timestamp': timestamp}
			self.update_neighbors(node_id, neighbors)
			return 1

	def remove_node(self, node_id):
		status = self.node_list.pop(node_id, 0)
		if status == 0:
			print('node removal failed, node_id given was not in the graph.')
			return 0
		else:
			return 1