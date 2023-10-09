# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import random
import socket
import struct
import sys
import argparse
from numpy.random import default_rng
import json

import networkx as nx

def raw_json_to_nx(jsonData):
  # Create an empty graph object
  G = nx.Graph()
  # Loop through the nodes in the JSON object and add them to the graph object
  for node in jsonData['nodes']:
    # Extract the node attributes from the list
    ip_address = node[0]
    color = node[1]
    size = node[2]
    labels = node[3]
    # Create a dictionary of node attributes
    node_attr = {'ip_address': ip_address, 'color': color, 'size': size, 'labels': labels}
    # Add the node and its attributes to the graph object
    G.add_node(ip_address, **node_attr)
  # Loop through the edges in the JSON object and add them to the graph object
  for edge in jsonData['edges']:
    # Extract the edge attributes from the list
    source_ip = edge[0]
    target_ip = edge[1]
    byte_weight = edge[2]
    connection_weight = edge[3]
    packet_weight = edge[4]
    # Create a dictionary of edge attributes
    edge_attr = {'source_ip_address': source_ip, 'target_ip_address': target_ip, 'byte_weight': byte_weight, 'connection_weight': connection_weight, 'packet_weight': packet_weight}
    # Add the edge and its attributes to the graph object
    G.add_edge(source_ip, target_ip, **edge_attr)
  # Return the graph object
  return G


def raw_json_to_nx_json(rawJsonData):
  nxGraph = raw_json_to_nx(rawJsonData)
  nx_json = nx.node_link_data(nxGraph)
  return nx_json

def generate_mock_graph(numNodes, numVnets, degreeOfConnectivity, outFilename):
    # Generate random prefixes one for each vnet
    # prefixes = [random.randint(1, 0xffffffff) & 0xffff0000 for i in range(0, numVnets)]

    # Generate random prefixes one for each vnet but have to include 149.196 and 15.76 and 10.55 in the prefixes
    prefixes = [random.choice([0x95c4, 0x0f4c, 0x0a37]) << 16 for i in range(0, numVnets - 3)]

    # Generate random IPs with one of the vnet prefixes
    suffixes = [random.randint(1, 0xffff) for i in range(0, numNodes)]

    ips = [socket.inet_ntoa(struct.pack('>I', random.choice(prefixes) | suffix)) for suffix in suffixes]
        
    macs = ['%012x' % random.randrange(16**12) for i in range(0, numNodes)]
    rng = default_rng()
    byteWeights = rng.exponential(0.5,[numNodes,numNodes])
    connWeights = rng.exponential(1,[numNodes,numNodes])
    pktWeights = rng.exponential(1.5,[numNodes,numNodes])

    edges = []
    nodes = []

    # Add a default color, size and label to each ip and append to nodes
    for ip in ips:
        nodes.append([ip, 'steelblue', 4, ['type=VM']])

    for i in range(0, numNodes):
        for j in range(0, numNodes):

            if i == j:
                continue

            if random.uniform(0,1) < degreeOfConnectivity:
                #row = ['2022-11-23 17:00:00.000', macs[i], macs[j], ips[i], ips[j], 'I', 'A', 'ew', byteWeights[i,j], connWeights[i,j], pktWeights[i,j]]
                row = [ips[i], ips[j], byteWeights[i,j], connWeights[i,j], pktWeights[i,j]]
                edges.append(row)

    # The edges generated above are part of the directed graph, consolidate them as undirected edges
    # For each edge check if an edge in the same or reverse direction exists in the dict undirected edges, if so, instead of adding
    # this edge to the dict, add the byte, conn and pkt weights to the existing edge
    undirectedEdges = {}
    for edge in edges:
        key = edge[0] + edge[1]
        reverseKey = edge[1] + edge[0]
        if key in undirectedEdges:
            undirectedEdges[key][2] += edge[2]
            undirectedEdges[key][3] += edge[3]
            undirectedEdges[key][4] += edge[4]
        elif reverseKey in undirectedEdges:
            undirectedEdges[reverseKey][2] += edge[2]
            undirectedEdges[reverseKey][3] += edge[3]
            undirectedEdges[reverseKey][4] += edge[4]
        else:
            undirectedEdges[key] = edge

    # add nodes and undirectedEdges to a dict and write to  file with path specified 
    # in args.outFilename using json package
    data = {"nodes" : nodes,
            "edges" : list(undirectedEdges.values())}
    
    nxGraph = raw_json_to_nx(data)
    nxNodeLinkJson = nx.node_link_data(nxGraph)
    
    with open(outFilename, "w") as f:
        json.dump(nxNodeLinkJson, f)

def parse_args():
    parser = argparse.ArgumentParser(prog = sys.argv[0])
    parser.add_argument('-n', '--nodes', dest='numNodes', help='number of nodes in the graph')
    parser.add_argument('-v', '--vnets', dest='numVnets', help='number of vnets in the graph')
    parser.add_argument('-c', '--connectivity', dest='degreeOfConnectivity', help='Degree of node connectivity [0,1] default=0.5. E.g., if set to 1, all nodes are connected to each other hence, n^2 edges will be generated for n nodes')
    parser.add_argument('-o', '--output', dest='outFilename', help='path to the output CSV file')

    args = parser.parse_args()
    valid_args = True

    if not args.numNodes:
        print("Please specify number of nodes to generate.")
        valid_args = False
        parser.print_help()
        sys.exit(1)

    if not args.numVnets:
        print("Please specify number of vnets to generate.")
        valid_args = False
        parser.print_help()
        sys.exit(1)
    
    if not args.degreeOfConnectivity:
        print("Defaulting to node connectivity of 0.5")
        args.degreeOfConnectivity = "0.5"
    
    if not args.outFilename:
        print("Output will be written to file ./mock_graph.json")
        args.outFilename = "./mock_graph.json"

    if not valid_args:
        parser.print_help()
        sys.exit(1)

    return args


if __name__=="__main__":    
    args = parse_args()
    numNodes = int(args.numNodes)
    numVnets = int(args.numVnets)
    degreeOfConnectivity = float(args.degreeOfConnectivity)
    generate_mock_graph(numNodes, numVnets, degreeOfConnectivity, args.outFilename)
