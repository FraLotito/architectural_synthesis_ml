from expression_parser import Expression_parser

infix = "( A * B ) + ( C * D )" # SPACES BETWEEN THE SYMBOLS ARE NEEDED!
print("INPUT: " + infix + '\n')

expression = Expression_parser(infix)
computational_graph = expression.get_computational_graph()
ASAP = computational_graph.asap()
ALAP = computational_graph.alap(20)
LIST_L = computational_graph.list_l([('*', 3), ('+', 5), ('R', 3)])