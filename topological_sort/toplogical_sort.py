
import unittest


def is_cyclic_util(g,v,visited,processing):
	processing.add(v)

	for u in g[v]:
		if u in processing:
			return True
		elif u not in visited and is_cyclic_util(g,u,visited,processing):
			return True

	processing.remove(v)
	visited.add(v)

	return False

def is_cyclic(g):
	
	visited = set()
	processing = set()

	for v in g.keys():
		if v not in visited:
			if is_cyclic_util(g,v,visited,processing):
				return True
		

	return False


def topological_sort_util(g,v,visited,result):
	for u in g[v]:
		if u not in visited:
			topological_sort_util(g,u,visited,result)

	visited.add(v)
	result.append(v)

def topological_sort(g):
	if is_cyclic(g):
		return None

	visited = set()
	result = []

	for v in g.keys():
		if v not in visited:
			topological_sort_util(g,v,visited,result)

	return result




	


class Testing(unittest.TestCase):
    def test_is_topological_sort(self):
        g = {1:[]}
        self.assertEqual(topological_sort(g), [1])

        g = {1:[1]}
        self.assertEqual(topological_sort(g), None)

        g = {1:[],2:[]}
        self.assertEqual(topological_sort(g), [1,2])

        g = {1:[2],2:[]}
        self.assertEqual(topological_sort(g), [2,1])

        g = {1:[2],2:[1]}
        self.assertEqual(topological_sort(g), None)


        g = {1:[3],2:[3],3:[]}
        self.assertEqual(topological_sort(g), [3,1,2])

        g = {1:[3],2:[3],3:[1]}
        self.assertEqual(topological_sort(g), None)

        g = {1:[2],2:[],3:[1]}
        self.assertEqual(topological_sort(g), [2,1,3])

        g = {1:[2],2:[],3:[4],4:[]}
        self.assertEqual(topological_sort(g), [2,1,4,3])

    def test_is_cyclic(self):
        g = {1:[]}
        self.assertEqual(is_cyclic(g), False)

        g = {1:[1]}
        self.assertEqual(is_cyclic(g), True)

        g = {1:[],2:[]}
        self.assertEqual(is_cyclic(g), False)

        g = {1:[2],2:[]}
        self.assertEqual(is_cyclic(g), False)

        g = {1:[2],2:[1]}
        self.assertEqual(is_cyclic(g), True)


        g = {1:[3],2:[3],3:[]}
        self.assertEqual(is_cyclic(g), False)

        g = {1:[3],2:[3],3:[1]}
        self.assertEqual(is_cyclic(g), True)

        g = {1:[2],2:[],3:[1]}
        self.assertEqual(is_cyclic(g), False)

        g = {1:[2],2:[],3:[4],4:[]}
        self.assertEqual(is_cyclic(g), False)
