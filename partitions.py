#!/usr/bin/env python

try:
    import json
except ImportError:
    import simplejson as json

try:
    import hostlist
except ImportError:
    print("Please install python-hostlist")

import argparse

class PartitionsInventory(object):
    def __init__(self):
        self.inventory = {}
        self.cli_args()

	# Called with `--list`.
	if self.args.list:
		self.inventory = self.get_inventory()
	# Called with `--host [hostname]`.
	elif self.args.host:
		# Not implemented, since we return _meta info `--list`.
		self.inventory = self.empty_inventory()
	# If no groups or vars are present, return an empty inventory.
	else:
		self.inventory = self.empty_inventory()
	print json.dumps(self.inventory, sort_keys=True, indent=4, separators=(',', ': '))

    def cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action='store_true')
        parser.add_argument('--host', action='store')
        self.args = parser.parse_args()

    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

    def get_inventory(self):
	partitions = []
	import os
	inventory_file = os.path.splitext(__file__)[0] + '.conf'

	try:
		with open(inventory_file) as fp:
			for line in fp:
				partitions.append(line)
	except IOError:
		print("Please create a {} file".format(inventory_file))
		exit(1)

	return self.build_inventory(partitions)

    def build_inventory(self, partitions):
	inventory = {}

	list_partitions = []
	for partition in partitions:
		tmp = {}
		for resource in partition.split():
			name, value = resource.split('=')
			tmp[name] = value
		list_partitions.append(tmp)

	for partition in list_partitions:
		if partition['PartitionName'] is not None and partition['PartitionName'] not in inventory:
			inventory[partition['PartitionName']] = {}

		if 'children' not in inventory[partition['PartitionName']]:
			inventory[partition['PartitionName']]['children'] = []

		if 'hosts' not in inventory[partition['PartitionName']]:
			inventory[partition['PartitionName']]['hosts'] = []

		try:
			inventory[partition['PartitionName']]['hosts'].extend(hostlist.expand_hostlist(partition['Nodes']))
			tmp = sorted(list(set(inventory[partition['PartitionName']]['hosts'])))
			inventory[partition['PartitionName']]['hosts'] = tmp
		except KeyError:
			pass

		try:
			inventory[partition['PartitionName']]['children'].extend(partition['Children'].split(','))
			tmp = sorted(list(set(inventory[partition['PartitionName']]['children'])))
			inventory[partition['PartitionName']]['children'] = tmp
		except KeyError:
			pass

		inventory_vars = {}
		for k, v in partition.items():
			if k not in ['PartitionName', 'Nodes', 'Children']:
				inventory_vars[k] = v
		inventory[partition['PartitionName']]['vars'] = {}
		inventory[partition['PartitionName']]['vars'] = inventory_vars

	return inventory

if __name__ == '__main__':
    PartitionsInventory()
