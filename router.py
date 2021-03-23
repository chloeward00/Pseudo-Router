from collections import defaultdict
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


class Graph(object):

    def __init__(self):
        self.graph = defaultdict(dict)

    def add_edge(self, start_node, end_node, cost):  # ADD EDGE TO GRAPH
 
        self.graph[end_node][start_node] = cost
        self.graph[start_node][end_node] = cost # Adding nodes to graph. Bidirectional



    def return_graph(self):

        return self.graph # returns graph so that the router class can access it.

    def visualize_graph(self): # for use in network x when visualising graph

        return self.graph


class Router(object):

    def __init__(self, graph, start):
        self.graph = graph # this is the nested dictionary that i created in the graph class
        self.start = start

    def get_nodes(self,graph): # getting nodes used for graph by using set etc to get ABCDEF

        key = set(self.graph.keys()) # using set so I get each letter only once

        for node in self.graph.values():


            if isinstance(node, dict):

                key |= node.keys()

        nodes = (sorted(key))
       
        return nodes
       

    def find_route(self, end): # DIKISTRAS  SHORTEST PATH ALGORITHM
       
        nodes = self.get_nodes(self.graph)
   
        start = self.start # start variable in the letter inputted in main function

        all_nodes = {n: float("inf") for n in nodes} # assinging infinity to each node

        all_nodes[start] = 0  # setting start to 0

        encountered = {}  # dictionary of all the nodes that were encountered

        pnodes = {}  # predecessors

        while all_nodes:

            min_val = min(all_nodes, key=all_nodes.get)  # get smallest distance in dic with nodes that havent been used yet
            
            for next_node, _ in self.graph.get(min_val, {}).items():

                if next_node in encountered:

                    continue

                new_cost = all_nodes[min_val] + self.graph[min_val].get(next_node, float("inf")) # adding new distance to node not encountered yet list by replacing infinity 
                
                if new_cost < all_nodes[next_node]: # if the new distance is less than the old distance
                    
                    all_nodes[next_node] = new_cost # assign new distance to variable
                    
                    pnodes[next_node] = min_val
            
            encountered[min_val] = all_nodes[min_val]
            
            all_nodes.pop(min_val)
            
            if min_val == end: # if the current node is equal to end node then program stops
                
                break
       
        return pnodes, encountered # returns dict with parent nodes and encountered dict with distances
     

    @staticmethod # static method function

    def find_path(pnodes, start,end): # function finds path

        path = [end] # putting end as a list


        while True:

            key = pnodes[path[0]] # key is index 0 in list

            path.insert(0, key) # inserting key into path 

            if key == start: # if key is start node then fucntion stops

                break

        return path # returns path taken

    def get_data(self,end):

        start = self.start # start node as specified in main function

        p, v = self.find_route(end) # refers back to find_route function to find route
     
    
        journey = self.find_path(p, start, end) # gets the path as a list
    
        path = "->".join(journey) # joins path nodes take with ->
        
        data  = [start,end,v[end],path]
        
        return data


    def get_path(self,end): # printing data found such as start end path cost by calling from get data function

        data = self.get_data(end)
       
       
        print("Start: {}\nEnd: {}\nPath: {}\nCost: {}\n".format(data[0],data[1],data[2],data[3]))



    def remove_router(self,k): # removing router

       outside_keys = k # my graph is a nested dictionary so I have outside keys and inside keys inside of it so i have
       inside_keys = k # a series of for loops to remove variable k from the graph

       for key in outside_keys: #  this function uses for loops etc to access outside keys and
        self.graph.pop(key)  #      inside keys inside the nested dictionary that i created

       for key in self.graph:
        for key2 in inside_keys:
            if key2 in self.graph[key]:
                self.graph[key].pop(key2)
       return self.graph # returns the graph with k removed from both inside keys and outside keys in nested dictionary
 

    def print_routing_table(self): # prints the routing table using PANDAS from_dict


        li = [] 
        nodes = self.get_nodes(self.graph) # refers back to get nodes function

        for node in nodes:

            if node != self.start: # if node doesnt equal to start node

                li.append(self.get_data(node)) # append the nodes to a list
       
       
        d = {}

        for k,v in enumerate(li): # for loop that adds to a dictionary so my pandas printing will have same layout as shown in the spec
            d[k] = v

        n = pd.DataFrame.from_dict(d,orient="index",columns = ["From","To","Cost","Path"]) # adding column names to pandas printing

        return n

def main():

    graph = Graph()

    graph.add_edge("a", "b", 7) # MAKING GRAPH. Adding edges
    graph.add_edge("a", "c", 9)
    graph.add_edge("a", "f", 14)
    graph.add_edge("b", "c", 10)
    graph.add_edge("b", "d", 15)
    graph.add_edge("c", "d", 11)
    graph.add_edge("c", "f", 2)
    graph.add_edge("d", "e", 6)
    graph.add_edge("e", "f", 9)
    graph.add_edge("c", "a", 9)

    


    network = nx.Graph(graph.visualize_graph()) # USING networkx to visualise the graph.
    nx.draw(network,with_labels=True) # calling it here so that visual graph is created before i remove nodes from router
    plt.savefig("graph.png")
    

    router = Router(graph.return_graph(), "a")

    router2 = Router(graph.return_graph(),"b")

    router.get_path("f")

    router2.get_path("a")

    print(router.print_routing_table()) # PRINTING FIRST TABLE WITH START NODE A

    print(router2.print_routing_table())

    router.remove_router("c")

    print(router.print_routing_table()) # PRINTING FIRST TABLE WITH START NODE B
    plt.show() # Showing my networkx graph here because if i do plt.show() at the top the terminal will not print rest of main().
    
    # THIS PROGRAM IS BIDIRECTIONAL CAN GO FROM A,B TO B,A 



if __name__ == '__main__':
    main()