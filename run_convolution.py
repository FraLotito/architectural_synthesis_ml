import numpy as np
from conv_parser import Conv_parser

input_matrix = np.array([['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i']])
#input_matrix = np.array([['a', 'b', 'c'], ['d', 'e', 'f']])
kernel = np.array([['A', 'B'], ['C', 'D']])

conv_network = Conv_parser(input_matrix, kernel)
computational_graph = conv_network.get_computational_graph()
computational_graph.asap()
computational_graph.alap(100)
computational_graph.list_l([('*', 1), ('+', 5), ('R', 6)])