op2cost = {}
op2cost['+'] = 2
op2cost['-'] = 2
op2cost['*'] = 4
op2cost['/'] = 4
op2cost['R'] = 1

def cost(op):
    if op not in op2cost:
        op = 'R'
    return op2cost[op]