##############################################################################################################################
##      Dennis Tracy Ivy, Jr.
##      04/2/2014
##      self study of MIT 6.00
##      ps11 - optimization, dynamic programming, graphs, etc
##      http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-00sc-introduction-to-computer-science-and-programming-spring-2011/unit-3/lecture-24-avoiding-statistical-fallacies/MIT6_00SCS11_ps11.pdf
##############################################################################################################################
import string                                                                           #import libraries
from graph import *                                                                     #import custom classes
##############################################################################################################################
#  this function takes a file name and using the data contained there in, builds and returns a digraph
##############################################################################################################################
def load_map(mapFilename):                                                              #read from a file and create the graph

    print ("Loading map from file...")
    g=Digraph()                                                                         #create a graph object
    if type(mapFilename) != str:                                                        #test to ensure file exists
        raise FileNotFoundError("Trouble opening" + mapFilename)                        #if not throw an exception
    with open(mapFilename, 'r') as f:                                                   #open the file safely
        for line in f:                                                                  #read it a line at a time
            try:                                                                        #attempt to read from the file
                src,dest,dist,outdoor = line.split()                                    #split it up into variables
            except:                                                                     #if couldn't read from the file
                raise Exception("Trouble reading from file" + mapFilename)              #throw an exception
            src_node  = Node(src)                                                       #create some nodes
            dest_node = Node(dest)                                                      

            if not g.hasNode(src_node) : g.addNode(src_node)                            #if the nodes don't already exist
            if not g.hasNode(dest_node) : g.addNode(dest_node)                          #add them to the graph

            edge=WEdge(src_node,dest_node,dist,outdoor)                                 #create an edge
            g.addEdge(edge)                                                             #and add it to the graph as well
        
    #with open("graph.txt", 'w') as out:                                                #for debugging purposes
    #    out.write(str(g))                                                              #uncomment to write the graph to a file
    #print(g)                                                                           #or print it to the screen
    return g                                                                            #return the graph
##############################################################################################################################
#recursive function to find the shortest path thru the graph using brute force exhaustive depth first search
#inputs:
#       digraph         = a digraph representing the relationship between buildings on the campus of MIT and their connections
#       start           = a string representing the number of the building to start from
#       end             = a string representing the number of the building to travel to
#       maxTotalDist    = the maximum distance you're willing to walk to get from start to end
#       maxDistOutdoors = the maximum distance you're willing to travel outdoors to get from start to end
#       visited         = a list of nodes you've already visited, defaults to None
#       counter         = a counter allowing you to know when you've failed to find a valid path
#outputs:
#       returns a list of buildings describing the path you should take.  buildings are represented as strings.
#       ex: ['1','2','3','4','5']
#exceptions:raises an exception if the path is not found or the start/end nodes are not contained in the graph
##############################################################################################################################
def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors, visited=None, counter=0): 

    if visited == None : visited = []                                                   #initialize visited on our first trip thru
    try:
        start = Node(start)                                                             #create nodes for the given values
        end = Node(end)
    except:
        raise ChildProcessError('Unable to create nodes')
    if not ( digraph.hasNode(start) and digraph.hasNode(end) ):                         #and confirm that these nodes exist int the graph
        raise ValueError("Start or End does not exist")
    path = [str(start)]                                                                 #this is only EVER 1 node long???
    if start == end : return path                                                       #if we found it, start backtracking
    shortest = None                                                                     #initialize the shortest path
    bestPath = None                                                                     #initialize the best path value
 
    for node in digraph.childrenOf(start):                                              #for each child of the current node
        destination = node.getDestination()                                             #find out the destination

        if ( str(destination) not in visited ):                                         #check to see if we've been there before
            visited = visited + [str(destination)]                                      #if not, we plan to visit it now, so update the list
            newPath = bruteForceSearch(digraph,                                         #call the function with the same 
                                       destination,                                     #using the current child node
                                       end,                                             #the same end
                                       maxTotalDist,                                    #same maxtotaldist
                                       maxDistOutdoors,                                 #and same maxDistOutdoors
                                       visited,
                                       counter=counter+1)                                         #and the recently updated copy of the visited list
            if newPath == None :                                                        #when we cant find a way thru, newPath will be none so...
                continue                                                                #try the next child by breaking out of the loop
                                                                                        
            currentPath,outdoor=digraph.calcPathLength(path + newPath)                  #if we did find a way thru  
            if outdoor > maxDistOutdoors or currentPath > maxTotalDist:                 #check to see if its too long
                visited.remove(str(destination))                                        #necessary to avoid skipping over previously checked paths...
                continue                                                                #and if so, break out of the loop and try the next child

            currentPath, outdoor=digraph.calcPathLength(newPath)                        #if we made it thru AND it wasn't too big
            if bestPath == None or (currentPath < bestPath):                            #check to see if its our first time to get this far on this level, 
                shortest = newPath                                                      #OR if our currentPath is shorter than the best path found so far                
                bestPath,outdoor = digraph.calcPathLength(shortest)                     #and if so, update things accordingly
                
    if shortest != None:                                                                #check to make sure we found something
        return path + shortest                                                          #and if so return it
    else :                                                                              #if we didn't find a way thru for this level,
        if counter==0: raise ValueError                                                 #if we never found a solution, raise an error
        return None                                                                     #return none
##############################################################################################################################
#recursive function to find the shortest path thru the graph using directed depth first search w/memoization/dynamic programming
#inputs:
#       digraph         = a digraph representing the relationship between buildings on the campus of MIT and their connections
#       start           = a string representing the number of the building to start from
#       end             = a string representing the number of the building to travel to
#       maxTotalDist    = the maximum distance you're willing to walk to get from start to end
#       maxDistOutdoors = the maximum distance you're willing to travel outdoors to get from start to end
#       visited         = a list of nodes you've already visited, defaults to None
#       memo            = a dictionary of key value pairs describing how to get from node to node 
#       counter         = a counter allowing you to know when you've failed to find a valid path
#outputs:
#       returns a list of buildings describing the path you should take.  buildings are represented as strings.
#       ex: ['1','2','3','4','5']
#exceptions:raises an exception if the path is not found or the start/end nodes are not contained in the graph
##############################################################################################################################
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors,visited = None, memo = None, counter=0):

    if visited == None : visited = []                                                   #initialize visited on our first trip thru
    if memo == None : memo = {}                                                         #initialize the memo
    start = Node(start)                                                                 #create nodes for the given values
    end = Node(end)
    if not (digraph.hasNode(start) and digraph.hasNode(end)):                           #and confirm that these nodes exist int he graph
        raise ValueError("Start or End does not exist")
    path = [str(start)]                                                                 #this is only EVER 1 node long???
    if start == end : return path                                                       #if we found it, start backtracking
    shortest = None                                                                     #initialize the shortest path
    bestPath = None                                                                     #initialize the best path value
  
    for node in digraph.childrenOf(start):                                              #for each child of the current node
        destination = node.getDestination()                                             #find out the destination
        if ( str(destination) not in visited ):                                         #check to see if we've been there before
            visited = visited + [str(destination)]                                      #if not, we plan to visit it now, so update the list
            try:
                newPath = memo[str(destination),str(end)]
            except:
                newPath = directedDFS (digraph,                                     #call the function with the same 
                                       destination,                                     #using the current child node
                                       end,                                             #the same end
                                       maxTotalDist,                                    #same maxtotaldist
                                       maxDistOutdoors,                                 #and same maxDistOutdoors
                                       visited,                                         #and the recently updated copy of the visited list
                                       memo,                                            #and the potentially new memo.
                                       counter=counter+1)                               #and increment the counter

            if newPath == None :                                                        #when we cant find a way thru, newPath will be none so...
                continue                                                                #try the next child by breaking out of the loop
            
            currentPath,outdoor=digraph.calcPathLength(path + newPath)                  #if we did find a way thru  
            if outdoor > maxDistOutdoors or currentPath > maxTotalDist:                 #check to see if its too long
                visited.remove(str(destination))                                        #so we have to backtrack a little
                try:                                                                    #and remove any references to this node
                    del(memo[str(destination),str(end)])                                #in our visited and memo collections
                except:                                                                 #we use a try in case the item doesn't actually exist in memo
                    pass                                                                #if it doesn't exist, just do nothing
                continue                                                                #break out of the loop and try the next child

            currentPath, outdoor=digraph.calcPathLength(newPath)                        #if we made it thru AND it wasn't too big
            if bestPath == None or (currentPath < bestPath):                            #check to see if its our first time to get this far on this level, 
                shortest = newPath                                                      #OR if our currentPath is shorter than the best path found so far                
                bestPath,outdoor = digraph.calcPathLength(shortest)                     #and if so, update things accordingly
                memo[str(destination), str(end)] = newPath            
                
    if shortest != None:                                                                #when we've made it thru all the children,check to make sure we found something
        return path + shortest                                                          #and if so, add the current node and return it
    else :                                                                              #if we didn't find a way thru for this level,
        if counter==0: raise ValueError                                                 #check to see if we never found a solution...if not, raise an error
        return None                                                                     #return none
##############################################################################################################################    
#### The following unit tests are part of this assignment, though i extended them somewhat for my own debugging purposes
#### Uncomment below when ready to test
##############################################################################################################################
if __name__ == '__main__':
##    # Test cases
    LARGE_DIST = 1000000
    digraph = load_map("mit_map.txt")
####    # Test case 1
    print ("---------------")
    print ("Test case 1:")
    print ("Find the shortest-path from Building 32 to 56")
    expectedPath1 = ['32', '56']
    print ("Expected:    ", expectedPath1)
    brutePath1 = bruteForceSearch(digraph, '32', '56', LARGE_DIST, LARGE_DIST)
    print ("Brute-force: ", brutePath1)
    dfsPath1 = directedDFS(digraph, '32', '56', LARGE_DIST, LARGE_DIST)
    print ("DFS:         ", dfsPath1)
    #try:
    #    digraph.calcPathLength(expectedPath1, toPrint=True)
    #    digraph.calcPathLength(brutePath1, toPrint=True)
    #    digraph.calcPathLength(dfsPath1, toPrint=True)
    #except:
    #    print("Uh oh...problem somewhere!")
    #input()
    # Test case 2
    print ("---------------")
    print ("Test case 2:")
    print ("Find the shortest-path from Building 32 to 56 without going outdoors")
    expectedPath2 = ['32', '36', '26', '16', '56']
    print ("Expected:    ", expectedPath2)
    brutePath2 = bruteForceSearch(digraph, '32', '56', LARGE_DIST, 0)
    print ("Brute-force: ", brutePath2)
    dfsPath2 = directedDFS(digraph, '32', '56', LARGE_DIST, 0)
    print ("DFS:         ", dfsPath2)
    #try:
    #    digraph.calcPathLength(expectedPath2, toPrint=True)
    #    digraph.calcPathLength(brutePath2, toPrint=True)
    #    digraph.calcPathLength(dfsPath2, toPrint=True)
    #except:
    #    print("trouble right here in river city.")
##
##    # Test case 3
    print ("---------------")
    print ("Test case 3:")
    print ("Find the shortest-path from Building 2 to 9")
    expectedPath3 = ['2', '3', '7', '9']
    print ("Expected:    ", expectedPath3)
    brutePath3 = bruteForceSearch(digraph, '2', '9', LARGE_DIST, LARGE_DIST)
    print ("Brute-force: ", brutePath3)
    dfsPath3 = directedDFS(digraph, '2', '9', LARGE_DIST, LARGE_DIST)
    print ("DFS:         ", dfsPath3)

    #digraph.calcPathLength(expectedPath3, toPrint=True)
    #digraph.calcPathLength(brutePath3, toPrint=True)
    #digraph.calcPathLength(dfsPath3, toPrint=True)
#
#    # Test case 4
    print ("---------------")
    print ("Test case 4:")
    print ("Find the shortest-path from Building 2 to 9 without going outdoors")
    expectedPath4 = ['2', '4', '10', '13', '9']
    print ("Expected:    ", expectedPath4)
    brutePath4 = bruteForceSearch(digraph, '2', '9', LARGE_DIST, 0)
    print ("Brute-force: ", brutePath4)
    dfsPath4 = directedDFS(digraph, '2', '9', LARGE_DIST, 0)
    print ("DFS:         ", dfsPath4)

    #digraph.calcPathLength(expectedPath4, toPrint=True)
    #digraph.calcPathLength(brutePath4, toPrint=True)
    #digraph.calcPathLength(dfsPath4, toPrint=True)
#
#    # Test case 5
    print ("---------------")
    print ("Test case 5:")
    print ("Find the shortest-path from Building 1 to 32")
    expectedPath5 = ['1', '4', '12', '32']
    print ("Expected:    ", expectedPath5)
    brutePath5 = bruteForceSearch(digraph, '1', '32', LARGE_DIST, LARGE_DIST)
    print ("Brute-force: ", brutePath5)
    dfsPath5 = directedDFS(digraph, '1', '32', LARGE_DIST, LARGE_DIST)
    print ("DFS:         ", dfsPath5)
    #digraph.calcPathLength(expectedPath5, toPrint=True)
    #digraph.calcPathLength(brutePath5, toPrint=True)
    #digraph.calcPathLength(dfsPath5, toPrint=True)
##
##    # Test case 6
    print ("---------------")
    print ("Test case 6:")
    print ("Find the shortest-path from Building 1 to 32 without going outdoors")
    expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
    print ("Expected:    ", expectedPath6)
    brutePath6 = bruteForceSearch(digraph, '1', '32', LARGE_DIST, 0)
    print ("Brute-force: ", brutePath6)
    dfsPath6 = directedDFS(digraph, '1', '32', LARGE_DIST, 0)
    print ("DFS:         ", dfsPath6)
    #try:
    #    digraph.calcPathLength(expectedPath6, toPrint=True)
    #    digraph.calcPathLength(brutePath6, toPrint=True)
    #    digraph.calcPathLength(dfsPath6, toPrint=True)
    #except:
    #    print("error")
#
    # Test case 7
    print ("---------------")
    print ("Test case 7:")
    print ("Find the shortest-path from Building 8 to 50 without going outdoors")
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
    try:
        #print("trying brute force...")
        bruteForceSearch(digraph, '8', '50', LARGE_DIST, 0)
    except ValueError:
        bruteRaisedErr = 'Yes'
    
    try:
        #print("trying directedDFS...")
        directedDFS(digraph, '8', '50', LARGE_DIST, 0)
    except ValueError:
        dfsRaisedErr = 'Yes'
    
    print ("Expected: No such path! Should throw a value error.")
    print ("Did brute force search raise an error?", bruteRaisedErr)
    print ("Did DFS search raise an error?", dfsRaisedErr)

    # Test case 8
    print ("---------------")
    print ("Test case 8:")
    print ("Find the shortest-path from Building 10 to 32 without walking")
    print ("more than 100 meters in total")
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
    try:
    #    #print("trying brute force...")
        x=bruteForceSearch(digraph, '10', '32', 100, LARGE_DIST)    #assgning to a value just to see what happens
    except ValueError:
        bruteRaisedErr = 'Yes'    
    try:
        #print("trying directedDFS...")
        y=directedDFS(digraph, '10', '32', 100, LARGE_DIST)         #exception should be raised and handled and no value should be assigned?
    except ValueError:
        dfsRaisedErr = 'Yes'
    
    print ("Expected: No such path! Should throw a value error.")
    print ("Did brute force search raise an error?", bruteRaisedErr)
    print ("Did DFS search raise an error?", dfsRaisedErr)
