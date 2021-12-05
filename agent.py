# prob.py
# This is

import random
import numpy as np
import queue

from gridutil import *

from typing import Tuple


# class for the values of previous_locations dict
class PreviousLocation:
    def __init__(self, prev_loc: Tuple[int, int, str], action: str, cost: int):
        self.prev_loc = prev_loc
        self.action = action  # action that leads from prev loc to the location being th ekey
        self.cost = cost  # cost of reaching the location being the key in previous_locations, cost should equal the cost of reaching prev_loc + cost of action


def is_loc_equal_dir_agnostic(loc1, loc2):
    return loc1[0] == loc2[0] and loc1[1] == loc2[1]


def strip_dir_from_loc(loc_with_dir):
    return (loc_with_dir[0], loc_with_dir[1])


def next_loc_with_dir(loc_with_dir):
    loc_without_dir = strip_dir_from_loc(loc_with_dir)
    dir = loc_with_dir[2]
    next_loc = nextLoc(loc_without_dir, dir)
    return (next_loc[0], next_loc[1], dir)


action_costs = {
    '': 0,
    'turnleft': 5,
    'turnright': 2,
    'forward': 1,
}
next_loc_lambdas = {
    '': lambda location: location,
    'turnleft': lambda location: (location[0], location[1], leftTurn(location[2])),
    'turnright': lambda location: (location[0], location[1], rightTurn(location[2])),
    'forward': lambda location: next_loc_with_dir(location),
}


def update_previous_locations(previous_locations, location, new_cost):
    previous_locations[location].cost = new_cost
    for k, v in previous_locations.items():
        if v.prev_loc == location:
            update_previous_locations(previous_locations, k, new_cost + action_costs[v.action])


class Agent:
    def __init__(self, size, walls, loc: Tuple[int, int], direction: str, goal):
        self.size = size
        self.walls = walls
        # list of valid locations
        self.locations = list({*locations(self.size)}.difference(self.walls))
        # dictionary from location to its index in the list
        self.loc_to_idx = {loc: idx for idx, loc in enumerate(self.locations)}
        self.loc = loc
        self.dir = direction
        self.goal = goal

        self.t = 0
        self.action_iteration_index = 0
        self.path_iteration_index = 0
        self.path, self.actions = self.find_path()

    def __call__(self):
        action = self.actions[self.action_iteration_index]
        self.action_iteration_index += 1
        if action == 'forward':
            self.path_iteration_index += 1
        return action

    def find_path(self):

        any_way_to_goal_reached = False
        minimal_cost_of_reaching_goal = None
        goal_loc = None  # (x_goal, y_goal, dir)
        current_loc = (self.loc[0], self.loc[1], self.dir)  # (x,y,dir)
        q = queue.Queue()
        # values in the queue are the same type as goal_loc (x,y,dir) e.g.:
        # [(5,5,'N'),(5,5,'E'), (5,5,'W'), (4,5,'W'), (6,5,'E')]
        previous_locations = {current_loc: PreviousLocation(current_loc, '', 0)}
        # keys in previous_locations are the same type as goal_loc (x,y,dir) e.g. (5,5,'W') values are instances of PreviousLocation
        q.put(current_loc)
        while not q.empty():
            current_loc = q.get()
            prev_loc = previous_locations[current_loc]
            cost_of_achieving_current_loc = prev_loc.cost + action_costs[prev_loc.action]
            # continue if the cost of reaching the current location is worse than the cost of reaching the goal
            if any_way_to_goal_reached:
                if minimal_cost_of_reaching_goal < cost_of_achieving_current_loc:
                    continue

            if is_loc_equal_dir_agnostic(current_loc, self.goal):
                any_way_to_goal_reached = True
                if minimal_cost_of_reaching_goal is None or minimal_cost_of_reaching_goal > cost_of_achieving_current_loc:
                    goal_loc = current_loc
                    minimal_cost_of_reaching_goal = cost_of_achieving_current_loc
                continue

            for action in ['turnleft', 'turnright', 'forward']:
                next_loc = next_loc_lambdas[action](current_loc)
                # if tries to go into the wall
                if action == 'forward' and strip_dir_from_loc(next_loc) not in self.locations:
                    continue
                accumulated_cost = cost_of_achieving_current_loc + action_costs[action]
                if next_loc not in previous_locations:
                    previous_locations[next_loc] = PreviousLocation(current_loc, action, accumulated_cost)
                    q.put(next_loc)
                elif accumulated_cost < previous_locations[next_loc].cost:
                    previous_locations[next_loc] = PreviousLocation(current_loc, action, accumulated_cost)
                    # here we need to update the cost of all previous locations that lead to the next location
                    # by doing this we do not need to recheck all previously reached locations
                    update_previous_locations(previous_locations, next_loc, accumulated_cost)

        back_tracking_loc = goal_loc
        path = [strip_dir_from_loc(back_tracking_loc)]
        actions = []
        while previous_locations[back_tracking_loc].action != '':
            prev_loc = previous_locations[back_tracking_loc]
            if prev_loc.action == 'forward':
                path = [strip_dir_from_loc(prev_loc.prev_loc)] + path
            actions = [prev_loc.action] + actions
            back_tracking_loc = prev_loc.prev_loc

        return path, actions

    def get_path(self):
        return self.path[self.path_iteration_index:]
