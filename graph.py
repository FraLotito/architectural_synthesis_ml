from utils import cost

class Graph(object):

	def __init__(self, graph_dict=None):
		""" initializes a graph object 
			If no dictionary or None is given, 
			an empty dictionary will be used
		"""
		if graph_dict == None:
			graph_dict = {}
		self.__graph_dict = graph_dict
		self.vertices_symbols = {}
		self.no_incoming_edges = set()
		self.parents = {}

	def N(self):
		return len(self.vertices_symbols.keys())

	def vertices(self):
		""" returns the vertices of a graph """
		return list(self.vertices_symbols.keys())

	def edges(self):
		""" returns the edges of a graph """
		return self.__generate_edges()

	def add_vertex(self, vertex):
		""" If the vertex "vertex" is not in 
			self.__graph_dict, a key "vertex" with an empty
			list as a value is added to the dictionary. 
			Otherwise nothing has to be done. 
		"""
		
		idx, val = vertex
		if idx not in self.__graph_dict:
			self.__graph_dict[idx] = []
			self.no_incoming_edges.add(idx)
			self.parents[idx] = []
		self.vertices_symbols[idx] = val

	def add_edge(self, edge):
		""" assumes that edge is of type set, tuple or list; 
			between two vertices can be multiple edges! 
		"""
		(vertex1, vertex2) = tuple(edge)
		if vertex2 in self.no_incoming_edges:
			self.no_incoming_edges.remove(vertex2)
		if vertex1 in self.__graph_dict:
			self.__graph_dict[vertex1].append(vertex2)
			self.parents[vertex2].append(vertex1)
		else:
			self.__graph_dict[vertex1] = [vertex2]
			self.parents[vertex1] = [vertex2]

	def topological_sort_visit(self, v, visited, result):
		visited[v] = True
		for i in self.__graph_dict[v]:
			if not visited[i]:
				self.topological_sort_visit(i, visited, result)

		result.insert(0, v)

	def topological_sort(self):
		visited = {i: False for i in self.__graph_dict.keys()}

		result = []

		for v in self.__graph_dict.keys():
			if not visited[v]:
				self.topological_sort_visit(v, visited, result)

		return result


	def asap(self):
		print("----- ASAP Algorithm -----")
		ordering = self.topological_sort()
		T = [-1 for i in ordering]

		outputs = []

		last_memory_read = 0

		for i in range(len(ordering)):
			if i in self.no_incoming_edges:
				T[i] = last_memory_read + 1
				last_memory_read = T[i]
				o = (T[i], "Operation N_{} = {} (read from memory to register) scheduled at time t = {}".format(i, self.vertices_symbols[i], T[i]))
			else:
				T[i] = 1
				for p in self.parents[i]:
					T[i] = max(T[p] + cost(self.vertices_symbols[p]), T[i])

				o = (T[i], "Operation N_{} = N_{} {} N_{} (mathematical operator) scheduled at time t = {}".format(i, self.parents[i][0], self.vertices_symbols[i], self.parents[i][1], T[i]))

			outputs.append(o)

		outputs = sorted(outputs)

		for o in outputs:
			print(o[1])

		print("\nT = {}\n".format(T))
		return T

	def alap(self, latency_bound):
		print("----- ALAP Algorithm: latency bound = {} -----".format(latency_bound))
		import math

		ordering = self.topological_sort()
		T = [-1 for i in ordering]

		outputs = []

		last_memory_read = 0

		for i in range(len(ordering)-1, -1, -1):
			if len(self.__graph_dict[i]) == 0:
				T[i] = latency_bound
				o = (T[i], "Operation N_{} = N_{} {} N_{} (mathematical operator) scheduled at time t = {}".format(i, self.parents[i][0], self.vertices_symbols[i], self.parents[i][1], T[i]))
			else:
				
				T[i] = math.inf
				for n in self.__graph_dict[i]:
					T[i] = min(T[n] - cost(self.vertices_symbols[i]), T[i])

				if i in self.no_incoming_edges:
					T[i] = T[i] - last_memory_read
					last_memory_read += 1

					o = (T[i], "Operation N_{} = {} (read from memory to register) scheduled at time t = {}".format(i, self.vertices_symbols[i], T[i]))
				else:
					o = (T[i], "Operation N_{} = N_{} {} N_{} (mathematical operator) scheduled at time t = {}".format(i, self.parents[i][0], self.vertices_symbols[i], self.parents[i][1], T[i]))
			outputs.append(o)

		outputs = sorted(outputs)

		for o in T:
			if o < 0:
				print("IMPOSSIBLE TO SCHEDULE!\n")
				return -1
		
		for o in outputs:
			print(o[1])

		print("\nT = {}\n".format(T))
		return T

	def list_l(self, resources):
		print("---- LIST_L with resources {}".format(resources))
		#print(resources)
		from queue import PriorityQueue

		finish = PriorityQueue()
		vertices = self.__graph_dict.keys()

		resources_symbols = [i[0] for i in resources]

		MAX_WAITING = max([i[1] for i in resources]) + 1
		without_schedules = 0

		T = [-1 for _ in vertices]
		completed = [False for _ in vertices]

		outputs = []

		l = 1

		while T[-1] == -1 and without_schedules < MAX_WAITING:
			memory_full = False
			#print(l)
			registers_to_free = 0

			while not finish.empty():
				item = finish.get()
				if item[0] == l:
					for i in range(len(resources)):
						if resources[i][0] == item[1]:
							resources[i] = (item[1], resources[i][1] + 1)
							registers_to_free += 1
					completed[item[2]] = True
				elif item[0] > l:
					finish.put(item)
					break

			for i in range(len(resources)):
				if resources[i][0] == 'R':
					resources[i] = (resources[i][0], resources[i][1] + registers_to_free)

			for i in range(len(resources)):
				#print("TRY ", resources[i][0])
				candidates = 0
				resource = resources[i][0]
				availability = resources[i][1]

				for v in vertices:
					if candidates == availability:
						break

					if T[v] != -1:
						continue

					#print(resource, self.vertices_symbols[v])

					if resource == self.vertices_symbols[v] or (resource == 'R' and self.vertices_symbols[v] not in resources_symbols):
						pred_all_scheduled_and_completed = True
						for p in self.parents[v]:
							if T[p] == -1 or not completed[p]:
								pred_all_scheduled_and_completed = False
								break
						#print(pred_all_scheduled_and_completed)
						if pred_all_scheduled_and_completed:
							if ((resource == 'R' and self.vertices_symbols[v] not in resources_symbols)) and not memory_full:
								T[v] = l
								without_schedules = 0
								o = (T[v], "Operation N_{} = {} (read from memory to register) scheduled at time t = {}".format(v, self.vertices_symbols[v], T[v]))
								outputs.append(o)
								candidates+=1
								completed[v] = True
								#finish.put((l + cost(resources[i][0]), resources[i][0], v))
								memory_full = True
							elif ((resource == 'R' and self.vertices_symbols[v] not in resources_symbols)) and memory_full:
								continue
							else:
								T[v] = l
								without_schedules = 0
								o = (T[v], "Operation N_{} = N_{} {} N_{} (mathematical operator) scheduled at time t = {}".format(v, self.parents[v][0], self.vertices_symbols[v], self.parents[v][1], T[v]))
								outputs.append(o)

								candidates+=1
								finish.put((l + cost(resources[i][0]), resources[i][0], v))
					

				#print("scheduled ", candidates)
				resources[i] = (resources[i][0], resources[i][1] - candidates)
			l += 1
			without_schedules += 1


		outputs = sorted(outputs)

		for o in T:
			if o < 0:
				print("IMPOSSIBLE TO SCHEDULE!\n")
				return -1
		
		for o in outputs:
			print(o[1])

		print("\nT = {}\n".format(T))

		return T
		

	def __generate_edges(self):
		""" A static method generating the edges of the 
			graph "graph". Edges are represented as sets 
			with one (a loop back to the vertex) or two 
			vertices 
		"""
		edges = []
		for vertex in self.__graph_dict:
			for neighbour in self.__graph_dict[vertex]:
				if {neighbour, vertex} not in edges:
					edges.append({vertex, neighbour})
		return edges

	def __str__(self):
		res = "vertices: "
		for k in self.__graph_dict:
			res += "(" + str(k) + ", " + str(self.vertices_symbols[k] + ") ")
		res += "\nedges: "
		for edge in self.__generate_edges():
			res += str(edge) + " "
		return res
