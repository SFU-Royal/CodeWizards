from model.ActionType import ActionType
from model.Game import Game
from model.Move import Move
from model.Wizard import Wizard
from model.World import World
from model.LaneType import LaneType
from model.Message import Message
from model.Faction import Faction

from Common import (State,
                    StateMachine,
                    lane_keypoints,)

from Helper import (get_nearest_visiable_enemy,)

PATH_FINDING_EPS = 10.0

class StateGoToLane(State):
    def __init__(self, lane=LaneType.TOP):
        super(StateGoToLane, self).__init__()
        self.dest_lane = lane
        self.keypoints = lane_keypoints.get_lane_keypoints(self.dest_lane)
        self.current_index = 0

    def run(self, input):
        print("StateGoToLane")
        me = input["me"]
        game = input["game"]
        keypoint = self.keypoints[self.current_index]
        if me.get_distance_to(keypoint.x, keypoint.y) < PATH_FINDING_EPS:
            if self.current_index != len(self.keypoints):
                self.current_index = self.current_index + 1
            keypoint = self.keypoints[self.current_index]
        self.forward_speed = game.wizard_forward_speed
        self.turn_angle = me.get_angle_to(keypoint.x, keypoint.y)

    def next(self, input):
        me = input["me"]
        world = input["world"]
        minions = world.minions
        wizards = world.wizards
        nearest_enemy = get_nearest_visiable_enemy(me, minions, wizards)
        # TODO: switch to laning with better checking function
        if nearest_enemy is not None:
            return StateMachine.Laning
        else:
            return StateMachine.GoToLane
