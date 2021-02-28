from pythonds.basic import Stack
from graph import Graph
import numpy as np

class Conv_parser(object):

    def __init__(self, input, kernel):
        self.input = input
        self.kernel = kernel

    def get_computational_graph(self):
        m = self.input
        k = self.kernel

        graph = Graph()

        v = 0

        for i in range(m.shape[0] - k.shape[0] + 1):
            for j in range(m.shape[1] - k.shape[1] + 1):
                M = m[i:i+k.shape[0], j : j+k.shape[1]]

                ids = []
                
                for x in range(k.shape[0]):
                    for y in range(k.shape[1]):
                        graph.add_vertex((v, M[x, y]))
                        #print("AGGIUNGO {} {}".format(v, M[x, y]))
                        v += 1
                        graph.add_vertex((v, k[x, y]))
                        #print("AGGIUNGO {} {}".format(v, k[x, y]))
                        v += 1
                        graph.add_vertex((v, '*'))
                        #print("AGGIUNGO {} {}".format(v, '*'))
                        graph.add_edge((v-2, v))
                        graph.add_edge((v-1, v))
                        #print("EDGE {} {}".format(v-2, v))
                        #print("EDGE {} {}".format(v-1, v))
                        ids.append(v)
                        v += 1
                before = -1
                
                for x in range(1, len(ids)):
                    if before == -1:
                        graph.add_vertex((v, '+'))
                        #print("AGGIUNGO {} {}".format(v, '+'))
                        graph.add_edge((ids[x-1], v))
                        graph.add_edge((ids[x], v))
                        #print("EDGE {} {}".format(ids[x-1], v))
                        #print("EDGE {} {}".format(ids[x], v))
                        before = v
                        v += 1
                    else:
                        graph.add_vertex((v, '+'))
                        #print("AGGIUNGO {} {}".format(v, '+'))
                        graph.add_edge((ids[x], v))
                        graph.add_edge((before, v))
                        #print("EDGE {} {}".format(ids[x], v))
                        #print("EDGE {} {}".format(before, v))
                        before = v
                        v += 1
                
        
        return graph