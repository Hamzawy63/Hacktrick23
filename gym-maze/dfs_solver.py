import numpy as np
import copy
def logger(obj):
    print(obj)


class DfsAgent():
    def __init__(self):
        self.stack = []
        self.obstacles = set() # (index1, index2) 

        self.previous_state = None
        self.prevous_label = None


        self.visited = {}

        self.N = 10
        self.M = 10

        self.north = 'N'
        self.south = 'S'
        self.west = 'W'
        self.east = 'E'
        
    def select_action(self, state):
        
        agent_loc = (state[0][0], state[0][1])
        logger(agent_loc)
        agent_location_encoded = (agent_loc[0] * self.N + agent_loc[1])

        manhattan_distances = state[1] # relative manhattan distances to the rewards
        directions = state[2] #array of tuples of directions to the rewards


       
        logger(self.stack)
        logger("========```")
        logger(self.previous_state)
        logger(state)
        logger("========```")

        if (self.previous_state != None and np.array_equal(self.previous_state[0], state[0])):
            assert(self.visited[agent_loc] == True)
            logger("The damn state doesn't change")
            other_direction = self.get_destination_from_label()
            self.obstacles.add((agent_location_encoded, other_direction[0] * self.N + other_direction[1]))
            self.obstacles.add((other_direction[0] * self.N + other_direction[1], agent_location_encoded))
        else: 
            self.stack.append(agent_loc)
            self.visited[agent_loc] = True



        available_destinations = self.get_available_destinations(agent_loc)
        available_destinations = self.sort_destinations(state, available_destinations)
        for destination in available_destinations:
            if (destination not in self.visited):
                logger("Found unvisited destination: {}".format(destination))
                self.previous_state = copy.deepcopy(state)

                self.prevous_label = self.get_destination_label(agent_loc, destination)
                return self.get_destination_label(agent_loc, destination)
        
        # If we come here then this means that there are not aviailable directions

        self.stack.pop() # remove me
        logger("Popping from stack")
        logger("Going to parent")
        parent_location = self.stack.pop()
        while (parent_location == agent_loc):
            parent_location = self.stack.pop()
            Assert(False)
            logger("Popping from stack")

        # self.previous_state = state[:]
        self.previous_state = copy.deepcopy(state)
        self.get_destination_label(agent_loc, parent_location)

        return self.get_destination_label(agent_loc, parent_location)



    def get_available_destinations(self, current_location):
        row = current_location[0]
        col = current_location[1]

        available_destinations = []
        # west , up ,east, down 
        directions = [[-1, 0], [0, -1], [0, 1], [1, 0]]
        for direction in directions:
            if (row + direction[0] >= 0 and row + direction[0] < self.N and col + direction[1] >= 0 and col + direction[1] < self.M):
                if((row * self.N + col, (row + direction[0]) * self.N + (col + direction[1])) not in self.obstacles):
                    available_destinations.append((row + direction[0], col + direction[1]))
        return available_destinations
    
    def sort_destinations(self, state, destinations):
        manhattan_distances = state[1] # relative manhattan distances to the rewards
        directions = state[2] #array of tuples of directions to the rewards
        agent_location = (state[0][0], state[0][1])
        
        destination_scores = {'N': 0, 'S': 0, 'W': 0, 'E': 0}

        num_of_riddles = len(directions)
        for i in range(num_of_riddles):
            if (manhattan_distances[i] != -1):
                if (directions[i] == [0, 1]):
                    destination_scores['S'] += 2
                elif (directions[i] == [0, -1]):
                    destination_scores['N'] += 2
                elif (directions[i] == [1, 0]):
                    destination_scores['E'] += 2
                elif (directions[i] == [-1, 0]):
                    destination_scores['W'] += 2
                elif (directions[i] == [1, 1]):
                    destination_scores['E'] += 1
                    destination_scores['S'] += 1
                elif (directions[i] == [-1, -1]):
                    destination_scores['W'] += 1
                    destination_scores['N'] += 1
                elif (directions[i] == [1, -1]):
                    destination_scores['E'] += 1
                    destination_scores['N'] += 1
                elif (directions[i] == [-1, 1]):
                    destination_scores['W'] += 1
                    destination_scores['S'] += 1
                else:
                    raise Exception("Unknown direction ya zmely {}".format(directions[i]))
                
        def my_comparator(destination):
            label = self.get_destination_label(agent_location, destination)
            assert(label in ['N', 'S', 'W', 'E'])
            return destination_scores[label]

        sorted_list = sorted(destinations, key=my_comparator)
        
        return reversed(sorted_list)
        
                





    def get_destination_from_label(self):
        if (self.prevous_label == self.north):
            return (self.previous_state[0][0] , self.previous_state[0][1] - 1)
        elif (self.prevous_label == self.south):
            return (self.previous_state[0][0] , self.previous_state[0][1] + 1 )
        elif (self.prevous_label == self.west):
            return (self.previous_state[0][0] - 1 , self.previous_state[0][1] )
        elif (self.prevous_label == self.east):
            return (self.previous_state[0][0] + 1 , self.previous_state[0][1] )
        else:
            logger(self.prevous_label)
            raise Exception("Unknown direction")

    # gets the location and the destination and returns the label
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
            raise Exception("Unknown direction")