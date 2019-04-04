#!/usr/bin/env python
import sys
from netaddr import *
#import yaml
import ruamel.yaml as yaml

import os
import argparse
import uuid
import copy

# Defaults
NUMBER=2
CPU=1
DISK=10

parser = argparse.ArgumentParser(description="Generate skeleton")

parser.add_argument("--number", dest="node_count", default=2, type=int,
                    help="Number of nodes", required=True)
parser.add_argument("--address", dest="address", default="192.168.100.100",
                    help="Start IP address", required=True)

parser.add_argument("--cpu", dest="cpu", default=1024, type=int,
                    help="Number of CPU's")
parser.add_argument("--memory", dest="memory", default=1, type=int,
                    help="Memory")
parser.add_argument("--disk", dest="disk", default=10, type=int,
                    help="Disk size")

parser.add_argument("--out", dest="output_file", help="Output file for updated infrastructure YAML. Default is stdout.")

args = parser.parse_args()


template = """
name: ironic04-aio
vbmc: 192.168.10.204
vbmc_bridge: "{{global_host_bridge}}"
cpu: 2
memory: 6144
virtualization: kvm
fqdn: ironic04-aio
block_pool: "{{global_disk_pool_name}}"
network_device_list:
- device: eth0
  host_net_dev: "{{global_ironic_bridge}}"
  host_net_mac: 0c:c4:7a:bb:ff:f4
block_device_list:
- device: sda
  block_size: 40
  type: file
uefi: true
"""

template = yaml.load(template,yaml.RoundTripLoader)
nodes = []
node_index = 0
for node in range(args.node_count):
  # get ip address
  template = copy.deepcopy(template)
  template["name"] = "ironic%s" % node_index
  template["cpu"] = args.cpu
  template["memory"] = args.memory
  template["block_device_list"][0]["block_size"] = args.disk
  ip = IPAddress(args.address)
  ip.value = ip.value + node_index
  template["vbmc"] = str(ip)
  # get mac address
  mac=EUI(template["network_device_list"][0]["host_net_mac"])
  mac.value = mac.value + node_index
  mac.dialect = mac_unix_expanded
  template["network_device_list"][0]["host_net_mac"] = str(mac)
  nodes.append(template)
  node_index += 1

f = sys.stdout
if args.output_file is not None:
    f = open(args.output_file, "w")

yaml.dump(nodes, f,Dumper=yaml.RoundTripDumper,
          default_flow_style=False)

