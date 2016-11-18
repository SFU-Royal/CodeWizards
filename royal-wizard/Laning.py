from model.LaneType import LaneType
from model.ActionType import ActionType

from Common import (State,
                    StateMachine)

from Helper import (get_nearest_visible_enemy,)


class StateLaning(State):
    def __init__(self, lane=LaneType.TOP):
        super(StateLaning, self).__init__()
        self.current_lane = lane

    def run(self, input_dict):
        print("StateLaning")
        me = input_dict["me"]
        world = input_dict["world"]
        minions = world.minions
        wizards = world.wizards
        nearest_enemy = get_nearest_visible_enemy(me, minions, wizards)
        # TODO: the right way to lancing
        self.forward_speed = 0
        self.action = ActionType.MAGIC_MISSILE
        if nearest_enemy is not None:
            self.turn_angle = me.get_angle_to(nearest_enemy.x, nearest_enemy.y)
        else:
            self.turn_angle = 0

    def next(self, input_dict):
        me = input_dict["me"]
        world = input_dict["world"]
        minions = world.minions
        wizards = world.wizards
        nearest_enemy = get_nearest_visible_enemy(me, minions, wizards)
        # TODO: a better check for retreat
        if nearest_enemy is None:
            return StateMachine.GoToLane
        elif me.life < me.max_life * 0.25:
            return StateMachine.Retreat
        else:
            return StateMachine.Laning
