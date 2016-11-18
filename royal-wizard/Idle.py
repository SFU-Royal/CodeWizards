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

class StateIdle(State):
    def __init__(self):
        super(StateIdle, self).__init__()
        pass

    def run(self, input):
        print("StateIdle")
        pass

    def next(self, input):
        return StateMachine.Idle