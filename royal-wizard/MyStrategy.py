from model.Game import Game
from model.Move import Move
from model.Wizard import Wizard
from model.World import World

from enum import Enum

from Idle import StateIdle
from GoToLane import StateGoToLane
from Laning import StateLaning
from Retreat import StateRetreat
from SwitchLane import StateSwitchLane
from Feed import StateFeed
from Dead import StateDead

from Common import StateMachine


class WizardState(Enum):
    Idle = 0
    GoToLane = 1
    Laning = 2
    Retreat = 3
    SwitchLane = 4
    Feed = 5
    Dead = 6

StateMachine.Idle = StateIdle()
StateMachine.GoToLane = StateGoToLane()
StateMachine.Laning = StateLaning()
StateMachine.Retreat = StateRetreat()
StateMachine.SwitchLane = StateSwitchLane()
StateMachine.Feed = StateFeed()
StateMachine.Dead = StateDead()

state_machine = StateMachine(initial_state=StateMachine.GoToLane)


class MyStrategy(object):
    def move(self, me: Wizard, world: World, game: Game, move: Move):
        # Every tick, update state first
        state_machine.update_state(me, world, game)

        # Take action for this state
        state_machine.run(me, world, game)

        # Current state
        state = state_machine.get_state()

        # Move
        move.speed = state.forward_speed
        move.strafe_speed = state.strafe_speed
        move.turn = state.turn_angle
        move.action = state.action
