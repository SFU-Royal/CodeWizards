from model.LaneType import LaneType

from Common import (State,
                    StateMachine,
                    lane_keypoints,)

from Helper import (get_nearest_visible_enemy,)

PATH_FINDING_EPS = 10.0


class StateGoToLane(State):
    def __init__(self, lane=LaneType.TOP):
        super(StateGoToLane, self).__init__()
        self.dest_lane = lane
        self.keypoints = lane_keypoints.get_lane_keypoints(self.dest_lane)
        self.current_index = 0

    def run(self, input_dict):
        print("StateGoToLane")
        me = input_dict["me"]
        game = input_dict["game"]
        keypoint = self.keypoints[self.current_index]
        if me.get_distance_to(keypoint.x, keypoint.y) < PATH_FINDING_EPS:
            if self.current_index != len(self.keypoints):
                self.current_index += 1
            keypoint = self.keypoints[self.current_index]
        self.forward_speed = game.wizard_forward_speed
        self.turn_angle = me.get_angle_to(keypoint.x, keypoint.y)

    def next(self, input_dict):
        me = input_dict["me"]
        world = input_dict["world"]
        minions = world.minions
        wizards = world.wizards
        nearest_enemy = get_nearest_visible_enemy(me, minions, wizards)
        # TODO: switch to laning with better checking function
        if nearest_enemy is not None:
            return StateMachine.Laning
        else:
            return StateMachine.GoToLane
