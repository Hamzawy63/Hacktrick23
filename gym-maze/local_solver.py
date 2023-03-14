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

def logger(obj):
    print(obj)


dfs_agent = DfsAgent()
step = 0
def select_action(state):
        global step
        # time.sleep(0.05)
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



def local_inference(riddle_solvers):
    # lives_saved = 0
    # riddles_scores = 0 
    # actions = 0
    # time_taken = 0
    # total_score = (lives_saved * 1000)/actions + riddles_scores/(time_taken*10) 

    obv = manager.reset(agent_id)

    for t in range(MAX_T):
        print("Hamza==============")
        # Select an action
        state_0 = obv
        action, action_index = select_action(state_0) # Random action
        obv, reward, terminated, truncated, info = manager.step(agent_id, action)

        # logger("obv:\n {}".format(obv))
        # logger("reward:\n {}".format(reward))
        # logger("terminated:\n {}".format(terminated))
        # logger("truncated:\n {}".format(truncated))
        # logger("info:\n {}".format(info))

        if not info['riddle_type'] == None:

            solution = riddle_solvers[info['riddle_type']](info['riddle_question'])
            obv, reward, terminated, truncated, info = manager.solve_riddle(info['riddle_type'], agent_id, solution)

       
          

        # THIS IS A SAMPLE TERMINATING CONDITION WHEN THE AGENT REACHES THE EXIT
        # IMPLEMENT YOUR OWN TERMINATING CONDITION
        is_there_someone_to_rescue = False
        distances = obv[1]

        for i in range(len(distances)):
            if distances[i] != -1:
                is_there_someone_to_rescue = True
                break
        if np.array_equal(obv[0], (9,9)) and (not is_there_someone_to_rescue):
            manager.set_done(agent_id)
            break # Stop Agent

        if RENDER_MAZE:
            manager.render(agent_id)

        states[t] = [obv[0].tolist(), action_index, str(manager.get_rescue_items_status(agent_id))]       
        
    # print("Done: score", manager.get_score(agent_id))


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

    