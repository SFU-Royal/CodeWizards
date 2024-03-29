from model.LaneType import LaneType

from Common import (State,
                    StateMachine,
                    world_keypoints,)

from Helper import (get_nearest_visible_enemy,)

PATH_FINDING_EPS = 5.0


class StateGoToLane(State):
    def __init__(self, lane=LaneType.MIDDLE):
        super(StateGoToLane, self).__init__()
        self.dest_lane = lane
        self.keypoints = []
        self.current_index = 0

    def run(self, input_dict):
        # print("StateGoToLane")
        me = input_dict["me"]
        game = input_dict["game"]
        if len(self.keypoints) == 0:
            self.keypoints = world_keypoints.get_route(me, world_keypoints.get_lane_keypoint(self.dest_lane))
            lane_to_enemy_base = world_keypoints.get_route(world_keypoints.get_lane_keypoint(self.dest_lane), world_keypoints.get_base(1-me.faction))
            self.keypoints.extend(lane_to_enemy_base)

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
        buildings = world.buildings
        nearest_enemy = get_nearest_visible_enemy(me, minions, wizards, buildings)
        # TODO: switch to laning with better checking function
        if nearest_enemy is not None:
            return StateMachine.Laning
        else:
            return StateMachine.GoToLane
