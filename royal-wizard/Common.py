from model.ActionType import ActionType
from model.Game import Game
from model.Wizard import Wizard
from model.World import World
from model.LaneType import LaneType
from model.Faction import Faction

from Helper import (get_distance,
                    get_nearest_item,
                    shortest_path)

class StateMachine(object):
    def __init__(self, initial_state):
        self.current_state = initial_state

    def update_state(self, me: Wizard, world: World, game: Game):
        input_dict = {"me": me, "world": world, "game": game}
        self.current_state = self.current_state.next(input_dict)

    def get_state(self):
        return self.current_state

    def run(self, me: Wizard, world: World, game: Game):
        input_dict = {"me": me, "world": world, "game": game}
        self.current_state.run(input_dict)


class State(object):
    def __init__(self, forward_speed=0.0, strafe_speed=0.0, turn_angle=0.0):
        self.forward_speed = forward_speed
        self.strafe_speed = strafe_speed
        self.turn_angle = turn_angle
        self.action = ActionType.NONE

    def run(self, input_dict):
        pass

    def next(self, input_dict):
        pass


class KeyPoint(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.edges = []


class Edge(object):
    def __init__(self, distance, to):
        self.distance = distance
        self.to = to


class WorldKeypoints(object):
    def __init__(self):
        self.keypoints = []
        self.lane_keypoints = [[[] * 2] * 3]
        self.lane_keypoints[LaneType.TOP][Faction.ACADEMY] = KeyPoint(3400, 200)

    def add_keypoint(self, x, y):
        self.keypoints.append(KeyPoint(x, y))

    # link keypoints with index i and j
    def link(self, i, j):
        dist = get_distance(self.keypoints[i], self.keypoints[j])
        self.keypoints[i].edges.append(Edge(dist, j))
        self.keypoints[j].edges.append(Edge(dist, i))

    def get_lane_keypoint(self, lane=LaneType.TOP, faction=Faction.ACADEMY):
        return self.lane_keypoints[lane][faction]

    # return list of keypoints for shortest route from a to b
    def get_route(self, point_a, point_b):
        _, start, _ = get_nearest_item(point_a, self.keypoints)
        _, end, _ = get_nearest_item(point_b, self.keypoints)
        return shortest_path(self.keypoints, start, end)

# init keypoints of game world
world_keypoints = WorldKeypoints()
for y in range(3400, 200, -400):
    world_keypoints.add_keypoint(220, y)
for x in range(600, 3400, 400):
    world_keypoints.add_keypoint(x, 200)
for i in range(len(world_keypoints.keypoints)-1):
    world_keypoints.link(i, i+1)