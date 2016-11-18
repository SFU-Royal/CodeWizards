from model.LaneType import LaneType

from Common import (State,
                    StateMachine)

from Helper import (get_nearest_visible_enemy,)


class StateRetreat(State):
    def __init__(self, lane=LaneType.TOP):
        super(StateRetreat, self).__init__()
        self.current_lane = lane

    def run(self, input_dict):
        print("StateRetreat")
        me = input_dict["me"]
        world = input_dict["world"]
        game = input_dict["game"]
        minions = world.minions
        wizards = world.wizards
        nearest_enemy = get_nearest_visible_enemy(me, minions, wizards)
        # TODO: better checking function
        if nearest_enemy is not None:
            self.forward_speed = -game.wizard_backward_speed
        else:
            self.forward_speed = 0.0

    def next(self, input_dict):
        # TODO: a better check for retreat
        me = input_dict["me"]
        if me.life > me.max_life * 0.60:
            return StateMachine.GoToLane
        else:
            return StateMachine.Retreat
