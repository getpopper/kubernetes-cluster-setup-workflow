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

node_list = list()
node_cnt = int(os.environ['NODES'])

# Create the raw "PC" nodes
for _idx in range(0, node_cnt):
    node = request.RawPC('node_{}'.format(_idx))
    node.hardware_type = str(os.environ['NODE_HARDWARE'])
    node_list.append(node)

# Create a link between them
link1 = request.Link(members=node_list)

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
        'ansible_host': str(dict_response['rspec']['node'][0]['host']['@ipv4']),
        'ansible_user': os.environ['GENI_USERNAME']
    }
}

worker_hosts = {}
for _idx in range(1, len(dict_response['rspec']['node'])):
    worker_hosts['worker{}'.format(_idx)] = {
        'ansible_host': str(dict_response['rspec']['node'][_idx]['host']['@ipv4']),
        'ansible_user': os.environ['GENI_USERNAME']
    }
hosts_dict['workers']['hosts'] = worker_hosts


with open('ansible/hosts.yml', 'w') as f:
    yaml.dump(hosts_dict, f)
