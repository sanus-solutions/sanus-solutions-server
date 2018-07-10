import numpy as np
import time

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

	def update_node(embeddings, timestamp, node_id):
		try:
			self.node_list[node_id]['embeddings'] = embeddings
			self.node_list[node_id]['timestamp'] = timestamp
			return 1
		except KeyError:
			print('node does not exist in the graph.')
			return 0

	def check_breach(embeddings, timestamp, node_id):
		try:
			node = self.node_list[node_id]
		except KeyError:
			print('Node does not exist in the graph.')
			return 'Fail'
		neighbors = node['neighbors']
		
		return 0

	def add_node(node_id, neighbors, node_type, embeddings=None, timestamp=None):
		"""
		node_id should be a string
		neighbors should be list of node_id strings
		node_type should be a string
		embeddings and timestamp default to None
		"""
		try:
			temp = self.node_list[node_id]
			print('Node exists, with neighbors: ' + temp['neighbors'] + 'and type ' + temp['node_type'])
			return 0
		except KeyError:
			print('Adding node now.')
			self.node_list[node_id] = {'neighbors': neighbors, 'node_type': node_type, 'embeddings': embeddings, 'timestamp': timestamp}
			return 1

	def remove_node(node_id):
		status = self.node_list.pop(node_id, 0)
		if status == 0:
			print('node removal failed, node_id given was not in the graph.')
			return 0
		else:
			return 1