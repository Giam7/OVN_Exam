import json
import math
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import connection
import signal_information
import line
import node


from signal_information import SignalInformation
from node import Node
from line import Line
import json
from scipy import special

class Network(object):
    def __init__ (self , json_path ):
        node_json = json . load ( open ( json_path ,'r'))
        self . _nodes = {}
        self . _lines = {}
        self . _connected = False
        self . _weighted_paths = None
        self._route_space = None
        for node_label in node_json :
            # Create the node instance
            node_dict = node_json [ node_label ]
            node_dict ['label '] = node_label
            node = Node ( node_dict )
            self . _nodes [ node_label ] = node
            # Create the line instance
                for connected_node_label in node_dict [' connected_nodes ']:
                    line_dict ={}
                    line_label = node_label + connected_node_label
                    line_dict ['label '] = line_label
                    node_position = np. array ( node_json [ node_label ][ 'position '])
                    connected_node_position =np.array( node_json [ connected_node_label ][ 'position '])
                    line_dict ['length '] =np.sqrt (np.sum (( node_position - connected_node_position )**2))
                line = Line ( line_dict )
                self . _lines [ line_label ] = line
    @property
    def nodes ( self ):
        return self . _nodes
    @property
    def lines ( self ):
        return self . _lines

    @property
    def weighted_paths(self):
        return self._weighted_paths

    def set_weighted_paths(self, signal_power):
        if not self.connected:
            self.connect()
        node_labels = self.nodes.keys()
        pairs = []
        for label1 in node_labels:
            for label2 in node_labels:
                if label1 != label2:
                    pairs.append(label1 + label2)
    df = pd.DataFrame()
    paths = []
    latencies = []
    noises = []
    snrs = []
    for pair in pairs:
        for path in self.find_paths(pair[0], pair[1]):
            path_string = ''
            for node in path:
                path_string += node + '->'
            paths.append(path_string[: -2])
            # Propagation
            signal_information = SignalInformation(signal_power, path)
            signal_information = self.propagate(signal_information)
            latencies.append(signal_information.latency)
            noises.append(signal_information.noise_power)
            snrs.append(
                10 * np.log10(
                    signal_information.signal_power /
                    signal_information.noise_power
                )
            )
    df['path '] = paths
    df['latency '] = latencies
    df['noise '] = noises
    df['snr '] = snrs
    self._weighted_paths = df


    def draw ( self ):
        nodes = self . nodes
        for node_label in nodes :
            n0 = nodes [ node_label ]
            x0 = n0. position [0]
            y0 = n0. position [1]
            plt . plot (x0 ,y0 ,'go ',markersize =10)
            plt . text (x0 +20 , y0 +20 , node_label )
            for connected_node_label in n0. connected_nodes :
                n1 = nodes [ connected_node_label ]
                x1 = n1. position [0]
                y1 = n1. position [1]
                plt . plot ([x0 ,x1 ],[y0 ,y1],'b')
        plt. title ('Network ')
        plt. show ()
    def find_paths (self ,label1 , label2 ):
        cross_nodes = [key for key in self . nodes . keys ()
                        if (( key != label1 ) & ( key != label2 ))]
        cross_lines = self . lines . keys ()
        inner_paths = {}
        inner_paths ['0'] = label1
        for i in range (len ( cross_nodes )+1):
            inner_paths [ str(i +1)] = []
            for inner_path in inner_paths [str (i)]:
                inner_paths [str(i +1)]+=[ inner_path + cross_node
                    for cross_node in cross_nodes
                        if (( inner_path [ -1]+ cross_node in cross_lines ) &
                            ( cross_node not in inner_path ))]
        paths = []
        for i in range (len ( cross_nodes )+1):
            for path in inner_paths [str (i)]:
                if path [ -1] + label2 in cross_lines :
                    paths . append ( path + label2 )
        return paths


# noinspection PyUnreachableCode
def connect(self):
        nodes_dict = self . nodes
        lines_dict = self . lines
        for node_label in nodes_dict :
            node = nodes_dict [ node_label ]
            for connected_node in node . connected_nodes :
                line_label = node_label + connected_node
                line = lines_dict [ line_label ]
                line.successive [ connected_node ] = nodes_dict [ connected_node ]
                node.successive [ line_label ] = lines_dict [ line_label ]
                self.connected= True

    def propagate (self , signal_information ):
        path = signal_information . path
        start_node = self . nodes [ path [0]]
        propagated_signal_information =start_node.propagate(signal_information)
        return propagated_signal_information


def find_best_snr(self, input_node, output_node):
    all_paths = self.weighted_paths.path.values
    inout_paths = [path for path in all_paths
                   if ((path[0] == input_node) and (path[-1] == output_node))]
    inout_df = self.weighted_paths.loc[
        self.weighted_paths.path.isin(inout_paths)]
    best_snr = np.max(inout_df.snr.values)
    best_path = inout_df.loc[
        inout_df.snr == best_snr].path.values[0].replace('->', '')
    return best_path

def find_best_latency (self , input_node , output_node ):
    all_paths = self . weighted_paths . path . values
    inout_paths = [ path for path in all_paths
        if (( path [0]== input_node ) and ( path [ -1]== output_node ))]
    inout_df = self . weighted_paths .loc[
        self . weighted_paths . path . isin ( inout_paths )]
    best_latency = np.min ( inout_df . latency . values )
    best_path = inout_df .loc[
        inout_df . latency == best_latency ]. path . values [0]. replace ('->','')
    return best_path

def stream (self , connections , best ='latency '):
    streamed_connections = []
    for connection in connections :
        input_node = connection . input_node
        output_node = connection . output_node
        signal_power = connection . signal_power
        self.set_weighted_paths ( signal_power )
        if best == 'latency ':
            path = self . find_best_latency ( input_node , output_node )
        elif best == 'snr ':
            path = self . find_best_snr ( input_node , output_node )
        else :
            print ('ERROR : best input not recognized . Value :',best )
            continue
        in_signal_information = SignalInformation ( signal_power , path )
        out_signal_information = self . propagate ( in_signal_information )
        connection . latency = out_signal_information . latency
        noise = out_signal_information . noise_power
        connection .snr = 10* np. log10 ( signal_power / noise_power )
        streamed_connections . append ( connection )
    return streamed_connections

    def available_paths (self , input_node , output_node ):
        if self . weighted_paths is None :
            self . set_weighted_paths (1)
    all_paths = [ path for path in self . weighted_paths . path . values
            if (( path [0]== input_node ) and ( path [ -1]== output_node ))]
unavailable_lines = [ line for line in self . lines
    if self . lines [ line ]. state == 'occupied ']
        available_paths = []
        for path in all_paths :
    available = True
        for line in unavailable_lines :
            if line [0] + '->' + line [1] in path :
                available = False
            break
        if available :
            available_paths . append ( path )
            return available_paths
def find_best_snr (self , input_node , output_node ):
    available_paths = self . available_paths ( input_node , output_node )
    if available_paths :
        inout_df = self . weighted_paths .loc[
        self . weighted_paths . path . isin ( available_paths )]
        best_snr = np.max( inout_df .snr. values )
        best_path = inout_df .loc[
        inout_df .snr == best_snr ]. path . values [0]. replace ('->','')
    else :
        best_path = None
        return best_path
def find_best_latency (self , input_node , output_node ):
    available_paths = self . available_paths ( input_node , output_node )
    if available_paths :
        inout_df = self . weighted_paths .loc[
        self . weighted_paths . path . isin ( available_paths )]
        best_latency = np. min( inout_df . latency . values )
        best_path = inout_df .loc[
        inout_df . latency == best_latency ]. path . values [0]. replace ('->','')
    else :
        best_path = None
    return best_path
def stream (self , connections , best ='latency '):
    streamed_connections = []
        for connection in connections :
        input_node = connection . input_node
        output_node = connection . output_node
        signal_power = connection . signal_power
        self . set_weighted_paths (1)
        if best == 'latency ':
            path = self . find_best_latency ( input_node , output_node )
        elif best == 'snr ':
        path = self . find_best_snr ( input_node , output_node )
        else :
        print ('ERROR : best input not recognized . Value :',best )
        continue
        if path :
    in_signal_information = SignalInformation ( signal_power , path )
        out_signal_information =
        self . propagate ( in_signal_information , True )
        connection . latency = out_signal_information . latency
        noise_power = out_signal_information . noise_power
        connection .snr = 10* np. log10 ( signal_power / noise_power )
        else :
        connection . latency = None
        connection .snr = 0
        streamed_connections . append ( connection )
        return streamed_connections
    from random import shuffle
    network = Network ('nodes . json ')
    network . connect ()
    node_labels = list ( network . nodes . keys ())
    connections = []
    for i in range (1000):
    shuffle ( node_labels )
        connection = Connection ( node_labels [0] , node_labels [ -1] ,1)
    connections . append ( connection )
streamed_connections = network . stream ( connections , best ='snr ')
snrs =[ connection . snr for connection in streamed_connections ]
plt. hist (snrs , bins =10)
plt. title ('SNR Distribution ')
plt. show ()

def set_weighted_paths (self , signal_power ):
    if not self . connected :
        self . connect ()
        node_labels = self . nodes . keys ()
        pairs = []
    for label1 in node_labels :
        for label2 in node_labels :
        if label1 != label2 :
        pairs . append ( label1 + label2 )
        df = pd. DataFrame ()
        paths = []
        latencies = []
        noises = []
        snrs = []
        for pair in pairs :
            for path in self . find_paths ( pair [0] , pair [1]):
            path_string = ''
            for node in path :
                path_string += node + '->'
                                        paths . append ( path_string [: -2])
            # Propagation
            signal_information = SignalInformation ( signal_power , path )
            signal_information =
            self . propagate ( signal_information , occupation = False )
        latencies . append ( signal_information . latency )
            noises . append ( signal_information . noise_power )
        snrs . append (
        10* np. log10 ( signal_information . signal_power /
        signal_information . noise_power ))
df['path '] = paths
df['latency '] = latencies
df['noise '] = noises
df['snr '] = snrs
self . _weighted_paths = df
route_space = pd. DataFrame ()
route_space ['path '] = paths
for i in range (10):
    route_space [str(i)]= ['free ']* len( paths )
    self . _route_space = route_space