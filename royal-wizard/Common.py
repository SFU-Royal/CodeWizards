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
        self.lane_keypoints = [0, 0, 0]
        self.lane_keypoints[LaneType.TOP] = KeyPoint(200, 200)
        self.lane_keypoints[LaneType.MIDDLE] = KeyPoint(2000, 2000)
        self.lane_keypoints[LaneType.BOTTOM] = KeyPoint(3800, 3800)

    def add_keypoint(self, x, y):
        self.keypoints.append(KeyPoint(x, y))

    # link keypoints with index i and j
    def link(self, i, j):
        dist = get_distance(self.keypoints[i], self.keypoints[j])
        self.keypoints[i].edges.append(Edge(dist, j))
        self.keypoints[j].edges.append(Edge(dist, i))

    def get_lane_keypoint(self, lane=LaneType.TOP):
        return self.lane_keypoints[lane]

    # return list of keypoints for shortest route from a to b
    def get_route(self, point_a, point_b):
        _, start, _ = get_nearest_item(point_a, self.keypoints)
        _, end, _ = get_nearest_item(point_b, self.keypoints)
        return shortest_path(self.keypoints, start, end)

# init keypoints of game world
world_keypoints = WorldKeypoints()

# top lane
top_start = 0
for y in range(3400, 200, -100):
    world_keypoints.add_keypoint(200, y)
for x in range(300, 3400, 100):
    world_keypoints.add_keypoint(x, 200)
top_end = len(world_keypoints.keypoints)-1
for i in range(top_start, top_end-1):
    world_keypoints.link(i, i+1)

# mid lane
mid_start = len(world_keypoints.keypoints)
for i in range(3400, 500, -70):
    world_keypoints.add_keypoint(i, 4000 - i)
mid_end = len(world_keypoints.keypoints)-1
for i in range(mid_start, mid_end-1):
    world_keypoints.link(i, i+1)

# bottom lane
bottom_start = len(world_keypoints.keypoints)
for x in range(600, 3400, 100):
    world_keypoints.add_keypoint(x, 3800)
for y in range(3300, 600, -100):
    world_keypoints.add_keypoint(3800, y)
bottom_end = len(world_keypoints.keypoints)-1
for i in range(bottom_start, bottom_end-1):
    world_keypoints.link(i, i+1)


world_keypoints.link(top_start, mid_start)
world_keypoints.link(mid_start, bottom_start)
world_keypoints.link(top_end, mid_end)
world_keypoints.link(mid_end, bottom_end)

f1_base = len(world_keypoints.keypoints)
world_keypoints.add_keypoint(200, 3800)
world_keypoints.link(f1_base, top_start)
world_keypoints.link(f1_base, bottom_start)

f2_base = len(world_keypoints.keypoints)
world_keypoints.add_keypoint(3800, 200)
world_keypoints.link(f2_base, top_end)
world_keypoints.link(f2_base, bottom_end)
