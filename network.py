import json
import math
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random


from signal_information import SignalInformation
from node import Node
from line import Line

from scipy import special

class Network ( object ):
    def __init__ (self , json_path ):
        node_json = json.load ( open ( json_path ,'r'))
        self._nodes = {}
        self._lines = {}
    for node_label in node_json :
        # Create the node instance
        node_dict = node_json [ node_label ]
        node_dict ['label '] = node_label
        node = Node ( node_dict )
        self . _nodes [ node_label ] = node

        # Create the line instances
        for connected_node_label in node_dict [' connected_nodes ']:
            line_dict ={}
            line_label = node_label + connected_node_label
            line_dict ['label '] = line_label
            node_position = np. array ( node_json [ node_label ][ 'position '])
            connected_node_position =
                np.array( node_json [ connected_node_label ][ 'position '])
            line_dict ['length '] =
                np. sqrt (
                    np.sum (( node_position - connected_node_position )**2)
                )
            line = Line ( line_dict )
            self . _lines [ line_label ] = line
    @property
    def nodes ( self ):
        return self . _nodes
    @property
    def lines ( self ):
        return self . _lines
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

    def propagate (self , signal_information ):
        path = signal_information . path
        start_node = self . nodes [ path [0]]
        propagated_signal_information =start_node.propagate(signal_information)
        return propagated_signal_information