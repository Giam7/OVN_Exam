from matplotlib import pyplot as plt

import network
import signal_information
import numpy as np
import pandas as pd

network = network('nodes.json')
network . connect ()
node_labels = network . nodes . keys ()
pairs = []
for label1 in node_labels :
    for label2 in node_labels :
        if label1 != label2 :
            pairs . append ( label1 + label2 )
columns = ['path ','latency ','noise ','snr ']
df = pd.DataFrame ()
paths =[]
latencies = []
noises = []
snrs = []
for pair in pairs :
    for path in network . find_paths ( pair [0] , pair [1]):
        path_string = ''
        for node in path :
            path_string += node + '->'
        paths.append ( path_string [: -2])
    # Propagation
    signal_information = signal_information(1, path)
    signal_information = network.propagate(signal_information)
    latencies.append(signal_information.latency)
    noises.append ( signal_information .noise_power )
    snrs.append (10* np.log10(signal_information . signal_power / signal_information . noise_power))
df['path '] = paths
df['latency '] = latencies
df['noise '] = noises
df['snr '] = snrs


from random import shuffle
    network = Network ('nodes.json ')
    network.connect ()
    node_labels = list ( network . nodes . keys ())
    connections = []
    for i in range (100):
        shuffle ( node_labels )
        connection = Connection ( node_labels [0] , node_labels [ -1] ,1)
        connections . append ( connection )
streamed_connections = network . stream ( connections )
latencies =[ connection . latency for connection in streamed_connections ]
plt. hist ( latencies , bins =10)
plt. title ('Latency Distribution ')
plt. show ()
streamed_connections = network . stream ( connections , best ='snr ')
snrs =[ connection . snr for connection in streamed_connections ]
plt. hist (snrs , bins =10)
plt. title ('SNR Distribution ')
plt. show ()