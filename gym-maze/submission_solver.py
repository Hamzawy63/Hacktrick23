import sys
import numpy as np
import math
import random
import json
import requests

from riddle_solvers import *
from dfs_solver_efficient import BfsAgent

### the api calls must be modified by you according to the server IP communicated with you
#### students track --> 16.170.85.45
#### working professionals track --> 13.49.133.141

server_ip = '13.49.133.141'
# server_ip = '127.0.0.1'
# server_ip = '34.165.238.24'


def logger(obj):
    # print(obj)
    pass


dfs_agent = BfsAgent()
step = 0


def select_action(state):
    # This is a random agent 
    # This function should get actions from your trained agent when inferencing.

    global step
    step = step + 1
    logger("Step: {}".format(step))

    actions = ['N', 'S', 'E', 'W']
    random_action = dfs_agent.select_action(state)
    action_index = actions.index(random_action)
    return random_action, action_index


def move(agent_id, action):
    response = requests.post(f'http://{server_ip}:5000/move', json={"agentId": agent_id, "action": action})
    return response

def solve(agent_id,  riddle_type, solution):
    response = requests.post(f'http://{server_ip}:5000/solve', json={"agentId": agent_id, "riddleType": riddle_type, "solution": solution}) 
    logger(response.json()) 
    return response

def get_obv_from_response(response):
    directions = response.json()['directions']
    distances = response.json()['distances']
    position = response.json()['position']
    obv = [position, distances, directions] 
    return obv

        
def submission_inference(riddle_solvers):

    response = requests.post(f'http://{server_ip}:5000/init', json={"agentId": agent_id})
    obv = get_obv_from_response(response)

    while(True):
        # Select an action
        state_0 = obv
        action, action_index = select_action(state_0) # Random action
        response = move(agent_id, action)
        if not response.status_code == 200:
            logger(response)
            break

        obv = get_obv_from_response(response)
        logger(response.json())

        if not response.json()['riddleType'] == None:
            solution = riddle_solvers[response.json()['riddleType']](response.json()['riddleQuestion'])
            response = solve(agent_id, response.json()['riddleType'], solution)


        # THIS IS A SAMPLE TERMINATING CONDITION WHEN THE AGENT REACHES THE EXIT
        # IMPLEMENT YOUR OWN TERMINATING CONDITION

        is_there_someone_to_rescue = False
        distances = obv[1]

        for i in range(len(distances)):
            if distances[i] != -1:
                is_there_someone_to_rescue = True
                break

        # if not is_there_someone_to_rescue:
        #     response = requests.post(f'http://{server_ip}:5000/leave', json={"agentId": agent_id})
        #     break
                
        if np.array_equal(response.json()['position'], (9,9)) and (not is_there_someone_to_rescue):
            response = requests.post(f'http://{server_ip}:5000/leave', json={"agentId": agent_id})
            break


if __name__ == "__main__":
    
    agent_id = "2uV5bMhG1k" # new agent id 
    riddle_solvers = {'cipher': cipher_solver, 'captcha': captcha_solver, 'pcap': pcap_solver, 'server': server_solver}
    submission_inference(riddle_solvers)
    
