from model.ActionType import ActionType
from model.Game import Game
from model.Move import Move
from model.Wizard import Wizard
from model.World import World
from model.LaneType import LaneType
from model.Message import Message
from model.Faction import Faction

from Common import (State,
                    StateMachine)

from Helper import (get_nearest_visiable_enemy,)

class StateRetreat(State):
    def __init__(self, lane=LaneType.TOP):
        super(StateRetreat, self).__init__()

    def run(self, input):
        print("StateRetreat")
        me = input["me"]
        world = input["world"]
        game = input["game"]
        minions = world.minions
        wizards = world.wizards
        nearest_enemy = get_nearest_visiable_enemy(me, minions, wizards)
        # TODO: better checking function
        if nearest_enemy is not None:
            self.forward_speed = -game.wizard_backward_speed
        else:
            self.forward_speed = 0.0

    def next(self, input):
        # TODO: a better check for retreat
        me = input["me"]
        if me.life > me.max_life * 0.60:
            return StateMachine.GoToLane
        else:
            return StateMachine.Retreat
