# Jason Wong
# 7.14 Escape Route Problem : Given a graph with population nodes P and safe zones S, check if there it is a valid graph
# where each P node travels along a path to a S node, however no P node can travel the same path as another P node. 
# Working to show if a graph is valid or not
from timeit import timeit


pop = ['A','B','S','D','M','F','Z','C','O','I','U','R']
safe = [1,2,3,4,5,6,7,8,9,10,11,12,13]
n = len(pop) + len(safe)
'''
edges = {'source': ['P1', "P2", 'P3'], 'sink': [], 'P1': ['S1', 'S2'], 'P2': ['S2'], 'P3': ['S1', 'S3'], 'S1': ['sink'], 'S2':['sink'], 'S3':['sink']} #Manual entry of the graph
nodes = ["source", "P1", "P2", "P3", "S1", "S2", 'S3']
print("Graph:", edges)
print("Nodes:", nodes)
'''

def graph(pop, safe): # This was used to make the graph by just linking them to all safe houses, did not realize the graph was suppose to be premade for this problem so enter manual if you want to do it like that
    #if len(pop) != len(safe):     Use this if you want the same pop nodes and safe nodes 
       #return "not equal"
    nodes = ["source", 'sink'] # source and sink for graph
    edges = {'source':[], 'sink':[]} # Edges for the graph
    for p in pop:
        nodes.append(p) # Connecting source to each pop
        edges[p] = []
        edges['source'].append(p) #connceting population areas to the srouce
        for c in safe:
            edges[p].append(c)   #connects the population to every safe place
    for s in safe:
        nodes.append(s)
        edges[s] = []
        edges[s].append('sink')
    print("GRAPH: ", edges)
    
    print("NODES: ",nodes)
    return flow(nodes, edges) == len(pop)

#https://pythoninwonderland.wordpress.com/2017/03/18/how-to-implement-breadth-first-search-in-python/ 
def bfs(edges, start, goal): # Breadth first search that goes through the graph 
    # keep track of explored nodes
    explored = []
    # keep track of all the paths to be checked
    queue = [[start]]
 
    # return path if start is goal
    if start == goal:
        return "DONE"
 
    # keeps looping until all possible paths have been checked
    while queue:
        # pop the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        if node not in explored:
            neighbours = edges[node]
            # go through all neighbour nodes, construct a new path and
            # push it into the queue
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                # return path if neighbour is goal
                if neighbour == goal:
                    return new_path
 
            # mark node as explored
            explored.append(node)
 
    # in case there's no path between the 2 nodes
    return False
    #return ('source','A')

# snippets of flow and augment function were taken from Aron's light and switch code, was modified to work in this problem
def flow(nodes, edges):
    
    f = {(False):None}  #creates dictionary of flow with all possible routes 
    for n in nodes:
        for e in edges[n]:
            f[(n,) + (e,)] = 0
            f[(e,)+(n,)] = None
    max_flow = 0
    p = (bfs(edges, 'source', 'sink'))
    
    print('------------------------------------------')
    
    while p:
        for x in p: #Will check the bfs path to see if it contains more than one population node
            count = 0
            if x in pop:
                count += 1
        if count > 1:
            print("Path contains more than one population node")
        else:
            print(p)
            f = augment(f,p)
            for i in range(0, len(p) -1): #updates edges
                
                edges[p[i]].remove(p[i+1]) #Always reverse the edge, since f(e) = 1
                edges[p[i+1]].append(p[i])
                
            p = (bfs(edges, 'source', 'sink')) # Goes to a new path
            if p == False:
                print("All paths done")
           
            max_flow += 1 
    print('------------------------------------------')
    print('FLOW DICTIONARY')
    print(f)
    print('------------------------------------------')
    print("Number of population zones that are safe: ", max_flow) 
    if max_flow == len(pop): #Checks to see if each population has gotten to a safe house
        print("All population safe")
    else:
        print("All population not safe")
        
    return max_flow

def augment(f,p): #O(e) = O(n) since p has at most n-1 edges
    
    b = 1 #bottleneck always equals 1 here
    for i in range(0,len(p)-1): #Update f(e) along the path
        
        #O(e)
        if f[(p[i],)+(p[i+1],)] != None: #If e is forward
            f[(p[i],)+(p[i+1],)]+=b
        else: #If e is backward
            f[(p[i+1],)+(p[i],)]-=b
    return f #f' the updated flow graph

def wrapper(func, *args): #wraps a function to allow the timeit function to use it 
    def wrapped():          #credit to Brandon Chupp for deciphering this
        return func(*args)
    return wrapped
    
    
#x = wrapper(graph, pop, safe) #passes our NewSan function through the wrapper
#print("Ford Fulkerson: size:", n, "time:", timeit(x, number = 1000)/1000)
#print(flow(nodes, edges)) #use this if entered manually 
(graph(pop,safe)) # use if using graph function to make the graph for you