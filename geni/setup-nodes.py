import os

# install packages
os.system('pip install PyYAML xmltodict')

import yaml
import xmltodict

import geni.portal as portal
import geni.rspec.pg as rspec

from geni import util
from geni.aggregate import cloudlab

request = portal.context.makeRequestRSpec()

# Create three raw "PC" nodes
node1 = request.RawPC("node1")
node2 = request.RawPC("node2")
node3 = request.RawPC("node3")

# Set each of the two to specifically request "m400" nodes, which in CloudLab, are ARM
node1.hardware_type = "m400"
node2.hardware_type = "m400"
node3.hardware_type = "m400"

# Create a link between them
link1 = request.Link(members = [node1, node2, node3])

# load context
ctx = util.loadContext(path="/geni-context.json",
                       key_passphrase=os.environ['GENI_KEY_PASSPHRASE'])

# create slice
util.createSlice(ctx, 'kube-cluster')

# create sliver on utah
manifest = util.createSliver(ctx, cloudlab.Utah, 'kube-cluster', request)

# generate ansible/hosts.yml file
hosts_dict = {
    'masters': {
        'hosts': None
    },
    'workers': {
        'hosts': None
    },
    'all': {
        'vars': {
            'ansible_python_interpreter': '/usr/bin/python3'
        }
    }
}

dict_response = xmltodict.parse(manifest.text)

hosts_dict['masters']['hosts'] = {
    'master': {
        'ansible_host': dict_response['rspec']['node'][0]['host']['@ipv4'],
        'ansible_user': os.environ['GENI_USERNAME']
    }
}

worker_hosts = {}
for _idx in range(1, len(dict_response['rspec']['node'])):
    worker_hosts['worker{}'.format(_idx)] = {
        'ansible_host': dict_response['rspec']['node'][_idx]['host']['@ipv4'],
        'ansible_user': os.environ['GENI_USERNAME']
    }
hosts_dict['workers']['hosts'] = worker_hosts


with open('ansible/hosts.yml', 'w') as f:
    yaml.dump(hosts_dict, f)
