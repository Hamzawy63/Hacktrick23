def logger(obj):
    print(obj)

class Graph():
    def __init__(self):
        self.graph = {}
        self.N = 10
        self.M = 10

        for i in range(self.N):
            for j in range(self.M):
                for dir in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    x = i + dir[0]
                    y = j + dir[1]
                    if (x >= 0 and x < self.N and y >= 0 and y < self.M):
                        self.add_bi_edge((i, j), (x, y))

    def add_bi_edge(self, u, v):
        
        if (u not in self.graph):
            self.graph[u] = set()

        if (v not in self.graph):
            self.graph[v] = set()

        self.graph[u].add(v)
        self.graph[v].add(u)

    def remove_edge(self, u, v):
       

        assert(u in self.graph)
        assert(v in self.graph)
        if (not (u in self.graph[v]) and (v in self.graph[u])):
            logger("Error: Removing a non-existent edge Or a directed edge")
            return

        self.graph[u].remove(v)
        self.graph[v].remove(u)

    def get_neighbours(self, u):
        return self.graph[u]



class BfsAgent():
    def __init__(self):
        self.obstacles = set() # (index1, index2) 

        self.graph = Graph()

        self.candidates = [set() for i in range(4)]

        self.previous_state = None
        self.prevous_label = None

        self.N = 10
        self.M = 10

        self.ENDING = (self.N - 1, self.M - 1)

        self.north = 'N'
        self.south = 'S'
        self.west = 'W'
        self.east = 'E'
    
    def get_potential_destinations(self, agent_loc, direction, manhattan_distance):
        if (manhattan_distance <= 0):
            return set()
        
        potential_destinations = set()
        queue = []
        visited = set()
        queue.append(agent_loc)
        visited.add(agent_loc)

        steps = 0
        while (len(queue) > 0):
            sz = len(queue)

            if (steps == manhattan_distance):
                break
            
            while(sz > 0):
                cur = queue.pop(0)

                for adj in self.graph.get_neighbours(cur):
                    if (adj not in visited):
                        queue.append(adj)
                        visited.add(adj)

                sz -=1

            steps +=1
        

        # Now we have all the locations that are at manhattan distance from the agent
        while (len(queue) != 0):
            cur = queue.pop(0)
            if (self.valid_orientation(agent_loc, cur, direction)):
                potential_destinations.add(cur)

        return potential_destinations

    def all_riddles_visited(self, manhattan_distances):
        for i in range(4):
            if (manhattan_distances[i] > 0):
                return False
        return True        

    def select_action(self,state):
        agent_loc = (state[0][0], state[0][1])
        direction = state[1]
        manhattan_distances = state[2]

        agent_previous_location = (self.previous_state[0][0], self.previous_state[0][1])

        if (self.previous_state != None and agent_loc == agent_previous_location):
            self.graph.remove_edge(agent_loc, agent_previous_location)
        

        # don't forget to store the previous state
        for i in range(4):
            potential_destinations = self.get_potential_destinations(agent_loc, direction[i], manhattan_distances[i])

            if (len(self.candidates[i]) == 0):
                self.candidates[i] = potential_destinations
            else:
                self.candidates[i] = self.candidates[i].intersection(potential_destinations) #wrong ?

        
        # Bfs to find 
        queue = []
        queue.append(agent_loc)
        visited = {}
        parent = {agent_loc: None}

        target = None
        while (len(queue) > 0):
            sz = len(queue)
            while (sz > 0):
                current = queue.pop(0)
                
                if (current in self.candidates[0] 
                    or current in self.candidates[1] 
                    or current in self.candidates[2] 
                    or current in self.candidates[3]
                    or (current == self.ENDING and self.all_riddles_visited(manhattan_distances) )):

                    target = current
                    break
                for neighbor in self.graph.get_neighbours(current):
                    if (neighbor not in parent):
                        parent[neighbor] = current
                        queue.append(neighbor)

                sz -= 1

        if (target != None):
            # get the parent and the direction 
            next_node = target
            while (parent[next_node] != agent_loc):
                next_node = parent[next_node]
        
            self.previous_state = state
            self.previous_label = self.get_destination_label(agent_loc, next_node)
            return self.previous_label
        else:
            assert(False)


    
    def get_destination_label(self, src, dst):
        diff = (dst[0] - src[0], dst[1] - src[1])
        if (diff == (-1, 0)):
            return self.west
        elif (diff == (1, 0)):
            return self.east
        elif (diff == (0, -1)):
            return self.north
        elif (diff == (0, 1)):
            return self.south
        else:
            logger(diff)
            logger("Error in get_destination_label: Unknown direction {}".format(diff))
        

    def valid_orientation(self, agent_loc, destination, direction):
        if (direction == [0, 1]): # S
            return agent_loc[0] == destination[0] and agent_loc[1] < destination[1]
        elif (direction == [0, -1]): # N
            return agent_loc[0] == destination[0] and agent_loc[1] > destination[1]
        elif (direction == [1, 0]): # E
            return agent_loc[0] < destination[0] and agent_loc[1] == destination[1]
        elif (direction == [-1, 0]): # W
            return agent_loc[0] > destination[0] and agent_loc[1] == destination[1]
        elif (direction == [1, 1]): # SE
            return agent_loc[0] < destination[0] and agent_loc[1] < destination[1]
        elif (direction == [-1, -1]): # NW
            return agent_loc[0] > destination[0] and agent_loc[1] > destination[1]
        elif (direction == [1, -1]): # NE
            return agent_loc[0] < destination[0] and agent_loc[1] > destination[1]
        elif (direction == [-1, 1]): # SW
            return agent_loc[0] > destination[0] and agent_loc[1] < destination[1]
        else:
            # Identical positions
            return True
        