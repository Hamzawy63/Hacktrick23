import sys
import numpy as np
import math
import random
import json
import requests
import time

import gym
import gym_maze
from gym_maze.envs.maze_manager import MazeManager
from riddle_solvers import *
from dfs_solver import DfsAgent

# constants
UP = 'N'
down = 'S'
left = 'W'
right = 'E'

# history elements 
step = 0
previous_state = None
previous_action = None
obstacles = set() # set of tuples (x,y , direction)
riddle_index = -1

# In case of production, just comment the function
# The function is used to print whatever is passed to it (string, object)
def logger(obj):
    print(obj)
    
# gets the smallest manhattan distances from the the given distances
# returns the index of the smallest distance and the distance itself
# returns -1 If all the array is -1 (no reward is found)
def get_smalleset_manhattan_distance(agent_location, directions, manhattan_distances):
    answer = 1000000000
    found = False
    answer_idx = -1
    for i in range(len(manhattan_distances)):
        if manhattan_distances[i] != -1 and manhattan_distances[i] < answer:
            answer = manhattan_distances[i]
            found = True
            answer_idx = i
            
    if found:
        return answer_idx, answer
    else:
        return -1


        
def reach_riddle(state):
    global riddle_index
    riddle_position = state[1][riddle_index]
    riddle_direction = state[2][riddle_index]




def handle_state_no_change():
    previous_agent_location = previous_state[0]
    
    if ((previous_agent_location[0], previous_agent_location[1], previous_action) in obstacles):
        print("Something wrong: the obstacle existed. However, the agent didn't care ")
    else:
        obstacles.add((previous_agent_location[0], previous_agent_location[1], previous_action))


dfs_agent = DfsAgent()

def select_action(state):
        global step
        # time.sleep(2)
        agent_location = state[0]
        manhattan_distances = state[1] # relative manhattan distances to the rewards
        directions = state[2] #array of tuples of directions to the rewards

        step = step + 1
        # if (step == 1000):
        #     time.sleep(5)
        #     exit()
        logger("Step: {}".format(step))
        logger("State: {}".format(state))
        logger("Agent location: {}".format(agent_location))
        logger("Manhattan distances: {}".format(manhattan_distances))
        logger("Directions: {}".format(directions))

        action = dfs_agent.select_action(state)

        actions = ['N', 'S', 'E', 'W']
        
        action_index = actions.index(action)

    

        logger("Recieved action is Action: {}".format(action))
        return action, action_index




# def select_action(state):

#     # sleep for one second
#     time.sleep(1.5)
#     global step
#     global previous_state
#     global previous_action
#     global riddle_index

#     step = step + 1

#     # check If the state didn't change 
#     if previous_state == state:
#         handle_state_no_change()

#     if riddle_index != -1:
#         reach_riddle(state)
#     else:
#         riddle_index = get_smalleset_manhattan_distance(state[0], state[2], state[1])[0]
#     agent_location = state[0]
#     manhattan_distances = state[1] # relative manhattan distances to the rewards
#     directions = state[2] #array of tuples of directions to the rewards

#     logger("Step: {}".format(step))
#     logger("Agent location: {}".format(agent_location))
#     logger("Manhattan distances: {}".format(manhattan_distances))
#     logger("Directions: {}".format(directions))

#     # Simple solution 
#     ## Pick the closest reward 
#     ## If there are multiple rewards at the same distance, pick any of them (temporarily)
#     ## Go to the corresponding diretions

#     # # Find the closest reward
#     closest_reward_idx, _ = get_smalleset_manhattan_distance(agent_location, directions, manhattan_distances)

#     # This is a random agent 
#     # This function should get actions from your trained agent when inferencing.
#     actions = ['N', 'S', 'E', 'W']
#     random_action = random.choice(actions)
    
#     while((agent_location[0], agent_location[1], random_action) in obstacles):
#         random_action = random.choice(actions)

        
#     action_index = actions.index(random_action)


#     # record the previous state
#     previous_state = state
#     previous_action = random_action

#     logger("Action: {}".format(random_action))
#     return random_action, action_index


def local_inference(riddle_solvers):

    obv = manager.reset(agent_id)

    for t in range(MAX_T):
        print("Hamza==============")
        # Select an action
        state_0 = obv
        action, action_index = select_action(state_0) # Random action
        obv, reward, terminated, truncated, info = manager.step(agent_id, action)

        if not info['riddle_type'] == None:
            solution = riddle_solvers[info['riddle_type']](info['riddle_question'])
            obv, reward, terminated, truncated, info = manager.solve_riddle(info['riddle_type'], agent_id, solution)
          

        # THIS IS A SAMPLE TERMINATING CONDITION WHEN THE AGENT REACHES THE EXIT
        # IMPLEMENT YOUR OWN TERMINATING CONDITION
        if np.array_equal(obv[0], (9,9)):
            manager.set_done(agent_id)
            break # Stop Agent

        if RENDER_MAZE:
            manager.render(agent_id)

        states[t] = [obv[0].tolist(), action_index, str(manager.get_rescue_items_status(agent_id))]       
        


if __name__ == "__main__":

    sample_maze = np.load("hackathon_sample.npy")
    agent_id = "9" # add your agent id here
    
    manager = MazeManager()
    manager.init_maze(agent_id, maze_cells=sample_maze)
    env = manager.maze_map[agent_id]

    riddle_solvers = {'cipher': cipher_solver, 'captcha': captcha_solver, 'pcap': pcap_solver, 'server': server_solver}
    maze = {}
    states = {}

    
    maze['maze'] = env.maze_view.maze.maze_cells.tolist()
    maze['rescue_items'] = list(manager.rescue_items_dict.keys())

    MAX_T = 5000
    RENDER_MAZE = True
    

    local_inference(riddle_solvers)

    with open("./states.json", "w") as file:
        json.dump(states, file)

    
    with open("./maze.json", "w") as file:
        json.dump(maze, file)
    