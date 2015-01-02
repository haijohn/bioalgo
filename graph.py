

"""implemnet three basic graph class Node, Edge, Graph
"""

class Node(object):

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

class Edge(object):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
    
    def get_src(self):
        return self.src
    
    def get_dest(self):
        return self.dest

    def __str__(self):
        return ' -> '.join([self.src.name,self.dest.name])

class WeightedEdge(Edge):
    def __init__(self, src, dest, weight):
        super(WeightedEdge, self).__init__(src,dest)
        self.weight = weight

    def get_weight(self):
        return self.weight

class DiGraph(object):
    def __init__(self):
        self.nodes = set()
        self.edges = {}

    def add_node(self, node):
        if node in self.nodes:
            raise Exception('duplicated node')
        else:
            self.nodes.add(node)
            self.edges[node] = []

    def add_edge(self, edge):
        src = edge.get_src()
        dest = edge.get_dest()
        if src not in self.nodes or dest not in self.nodes:
            raise Exception('node not in graph')
        else:
            self.edges[src].append(dest)

    def get_children(self, node):
        if node not in self.nodes:
            raise Exception('node not in graph')
        return set(self.edges[node])

    def outdegree(self,node):
        return len(self.edges[node]) 

    def get_parents(self, node):
        return {src_node for src_node in self.nodes 
                    if node in self.edges[src_node]}
            
    def indegree(self,node):
        return len([src_node for src_node in self.nodes 
                    if node in self.edges[src_node]])



            
        
