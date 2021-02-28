from pythonds.basic import Stack
from graph import Graph

class Expression_parser(object):

	def __init__(self, infix):
		self.infix = infix
		self.postfix = self.infixToPostfix(infix)

	def isOperator(self, c):
		if (c == '+' or c == '-' or c == '*'
				or c == '/' or c == '^'):
			return True
		else:
			return False

	def get_computational_graph(self):
		stack = []

		graph = Graph()
		i = 0

		for char in self.postfix:
			if not self.isOperator(char):
				graph.add_vertex((i, char))
				stack.append(i)
			else:
				graph.add_vertex((i, char))
				t1 = stack.pop()
				t2 = stack.pop()
				graph.add_edge((t1, i))
				graph.add_edge((t2, i))
				stack.append(i)

			i+=1

		return graph


	def infixToPostfix(self, infixexpr):
		prec = {}
		prec["*"] = 3
		prec["/"] = 3
		prec["+"] = 2
		prec["-"] = 2
		prec["("] = 1
		opStack = Stack()
		postfixList = []
		tokenList = infixexpr.split()

		for token in tokenList:
			if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "0123456789":
				postfixList.append(token)
			elif token == '(':
				opStack.push(token)
			elif token == ')':
				topToken = opStack.pop()
				while topToken != '(':
					postfixList.append(topToken)
					topToken = opStack.pop()
			else:
				while (not opStack.isEmpty()) and \
						(prec[opStack.peek()] >= prec[token]):
					postfixList.append(opStack.pop())
				opStack.push(token)

		while not opStack.isEmpty():
			postfixList.append(opStack.pop())
		return "".join(postfixList)