from model.ActionType import ActionType
from model.Game import Game
from model.Move import Move
from model.Wizard import Wizard
from model.World import World
from model.LaneType import LaneType
from model.Message import Message
from model.Faction import Faction

class StateMachine:
    def __init__(self, initial_state):
        self.current_state = initial_state

    def update_state(self, me: Wizard, world: World, game: Game):
        input = {"me": me, "world": world, "game": game}
        self.current_state = self.current_state.next(input)

    def get_state(self):
        return self.current_state

    def run(self, me: Wizard, world: World, game: Game):
        input = {"me": me, "world": world, "game": game}
        self.current_state.run(input)

class State:
    def __init__(self, forward_speed = 0.0, strafe_speed = 0.0, turn_angle = 0.0):
        self.forward_speed = forward_speed
        self.strafe_speed = strafe_speed
        self.turn_angle = turn_angle
        self.action = ActionType.NONE

    def run(self):
        pass

    def next(self, input):
        pass

class KeyPoint():
    def __init__(self, x, y):
        self.x = x;
        self.y = y

class LaneKeyPoints():
    def __init__(self):
        self.keypoints = [[], [], []]

    def update_keypoints(self, lane, keypoints):
        self.keypoints[lane] = keypoints

    def get_lane_keypoints(self, lane = LaneType.TOP):
        return self.keypoints[lane];

top_keypoints = []
for y in range(3400, 200, -400):
    top_keypoints.append(KeyPoint(220, y))
for x in range(600, 3400, 400):
    top_keypoints.append(KeyPoint(x, 200))

mid_keypoints = []
bot_keypoints = []

lane_keypoints = LaneKeyPoints()
lane_keypoints.update_keypoints(lane=LaneType.TOP, keypoints=top_keypoints)
lane_keypoints.update_keypoints(lane=LaneType.MIDDLE, keypoints=mid_keypoints)
lane_keypoints.update_keypoints(lane=LaneType.BOTTOM, keypoints=bot_keypoints)