#################################################
# term project: MyRoom
# agent.py
# version 22.12.07

# name: Felicia Luo
# andrew id: zhixinlu
#################################################

from utils.helperFn import sin, cos
import numpy as np
import copy

# CITATION: class Agent and Sweeper from https://github.com/dungba88/cleaner_robot
# I deleted and replaced some code with my own work listed below.

# My own work in this file: 
# class Node, Sweeper.adjacent_movable(),
# functions adjacent(), getLeftPos(), getRightPos()

class Agent():

    def __init__(self, room, start_node):
        self.room = room
        self.curr_node = start_node
        self.move_count = 0
        self.turn_count = 0
        self.loggable = False
        self.clr = 18
        self.roomLog = copy.deepcopy(room)
        self.roomLog[start_node.y, start_node.x] = 1

    def turn_left(self):
        """turn 90 degree counter-clockwise"""
        self.curr_node.dir = (self.curr_node.dir + 1) % 4
        self.turn_count += 1
        return self

    def turn_right(self):
        """turn 90 degree clockwise"""
        self.curr_node.dir = (self.curr_node.dir + 3) % 4
        self.turn_count += 1
        return self

    def move(self):
        """move ahead"""
        next_pos_x = self.curr_node.x + cos(self.curr_node.dir)
        next_pos_y = self.curr_node.y - sin(self.curr_node.dir)
        if not self.can_move(next_pos_x, next_pos_y):
            return False
        self.move_count += 1
        self.curr_node.x = next_pos_x
        self.curr_node.y= next_pos_y
        self.roomLog[next_pos_y, next_pos_x] = 1
        if self.loggable:
            self.log()
        return True

    def can_move(self, next_pos_x, next_pos_y):
        if next_pos_x < 0 or next_pos_y < 0:
            return False
        if next_pos_y >= self.room.shape[0]:
            return False
        if next_pos_x >= self.room.shape[1]:
            return False

        return self.room[next_pos_y, next_pos_x] == 0

    def log(self):
        for i in range(self.room.shape[0]):
            text = ""
            for j in range(self.room.shape[1]):
                if i == self.curr_node.y and j == self.curr_node.x:
                    if self.curr_node.dir == 0:
                        text += '>'
                    elif self.curr_node.dir == 1:
                        text += '^'
                    elif self.curr_node.dir== 2:
                        text += '<'
                    else:
                        text += 'v'
                elif self.roomLog[i, j] == 1:
                    text += '*'
                elif self.room[i, j] == 0:
                    text += '.'
                else:
                    text += '|'
            print(text)
        print('')


class Sweeper():
    def __init__(self, agent):
        self.curr_node = agent.curr_node
        self.observed_map = {agent.curr_node.y: {agent.curr_node.x: 1}}
        self.agent = agent

    def sweep(self):
        while self.move():
            pass

    def move(self):
        target_path = self.find_nearest_unvisited_pos()
        if not target_path:
            return False
        self.move_with_path(target_path)
        return True

    def find_nearest_unvisited_pos(self):
        return bfs(self.curr_node, self.node_unvisited, self.adjacent_movable)

    def node_unvisited(self, node):
        node_val = self.get_node_from_map(node)
        return node_val is None

    def adjacent_movable(self, node):
        node_val = self.get_node_from_map(node)
        if node_val == -1: return False

        # check if fit clearance
        left_collide = False
        right_collide = False
        for left_pos in getLeftPos(node, self.agent.clr):
            if not self.agent.can_move(left_pos[0], left_pos[1]): left_collide = True
        for right_pos in getRightPos(node, self.agent.clr):
            if not self.agent.can_move(right_pos[0], right_pos[1]): right_collide = True
        if left_collide and right_collide: return False

        return True
        

    def get_node_from_map(self, node):
        if not node.y in self.observed_map \
                or not node.x in self.observed_map[node.y]:
            return None
        return self.observed_map[node.y][node.x]

    def move_with_path(self, target_path):
        for path in reversed(target_path):
            left_turns = path - self.curr_node.dir
            if left_turns < 0:
                left_turns += 4
            for _ in range(left_turns):
                    self.turn_agent_left()
            self.move_agent()

    def move_agent(self):
        next_node = self.calculate_next_node()

        if not self.observed_map.get(next_node.y, None):
            self.observed_map[next_node.y] = {}

        if self.agent.move():
            # mark the point as visited
            self.observed_map[next_node.y][next_node.x] = 1
            self.curr_node = next_node
            return True
        # mark the point as inaccessible
        self.observed_map[next_node.y][next_node.x] = -1
        return False

    def calculate_next_node(self):
        next_pos_x = self.curr_node.x + cos(self.curr_node.dir)
        next_pos_y = self.curr_node.y - sin(self.curr_node.dir)
        next_node = Node(next_pos_x, next_pos_y, direction=self.curr_node.dir, parent=self.curr_node)
        return next_node

    def turn_agent_left(self):
        self.curr_node.dir = (self.curr_node.dir + 1) % 4
        self.agent.turn_left()

    def turn_agent_right(self):
        self.curr_node.dir = (self.curr_node.dir + 3) % 4
        self.agent.turn_right()



class Node():
    def __init__(self, x, y, direction=None, parent=None):
        self.x = x
        self.y = y
        self.dir = direction
        self.parent = parent

    def __eq__(self, other):
        return (isinstance(self, Node) and isinstance(other, Node) and \
                self.x == other.x and self.y == other.y)


def bfs(start_node, finish_check_fn, adjacent_check_fn):
    # this is just simple BFS implementation
    checked = {}
    queue = []
    queue.append(Node(start_node.x, start_node.y))

    while queue:
        curr_node = queue.pop(0)
        finished = finish_check_fn(curr_node)
        if finished:
            path = []
            while curr_node.parent:
                path.append(curr_node.dir)
                curr_node = curr_node.parent
            return path
        for node in adjacent(curr_node):
            key = str(node.x) + '_' + str(node.y)
            if not checked.get(key, None) \
                    and adjacent_check_fn(node):
                checked[key] = 1
                queue.append(node)

def adjacent(curr_node):
    # in bfs, favor left
    if curr_node.dir == 0:
        return [
            Node(curr_node.x, curr_node.y - 1, direction=1, parent=curr_node),
            Node(curr_node.x + 1, curr_node.y, direction=0, parent=curr_node),
            Node(curr_node.x, curr_node.y + 1, direction=3, parent=curr_node),
            Node(curr_node.x - 1, curr_node.y, direction=2, parent=curr_node),
        ]
    elif curr_node.dir == 1:
        return [
            Node(curr_node.x - 1, curr_node.y, direction=2, parent=curr_node),
            Node(curr_node.x, curr_node.y - 1, direction=1, parent=curr_node),
            Node(curr_node.x + 1, curr_node.y, direction=0, parent=curr_node),
            Node(curr_node.x, curr_node.y + 1, direction=3, parent=curr_node),
        ]
    elif curr_node.dir == 2:
        return [
            Node(curr_node.x, curr_node.y + 1, direction=3, parent=curr_node),
            Node(curr_node.x - 1, curr_node.y, direction=2, parent=curr_node),
            Node(curr_node.x, curr_node.y - 1, direction=1, parent=curr_node),
            Node(curr_node.x + 1, curr_node.y, direction=0, parent=curr_node),
        ]
    else:
        return [
            Node(curr_node.x + 1, curr_node.y, direction=0, parent=curr_node),
            Node(curr_node.x, curr_node.y + 1, direction=3, parent=curr_node),
            Node(curr_node.x - 1, curr_node.y, direction=2, parent=curr_node),
            Node(curr_node.x, curr_node.y - 1, direction=1, parent=curr_node),
        ]

def getLeftPos(curr_node, clr):
    result = []
    for i in range(1, clr+1):
        next_pos_x = curr_node.x - i * sin(curr_node.dir)
        next_pos_y = curr_node.y - i * cos(curr_node.dir)
        result.append((next_pos_x, next_pos_y))
    return result

def getRightPos(curr_node, clr):
    result = []
    for i in range(1, clr+1):
        next_pos_x = curr_node.x + i * sin(curr_node.dir)
        next_pos_y = curr_node.y + i * cos(curr_node.dir)
        result.append((next_pos_x, next_pos_y))
    return result
