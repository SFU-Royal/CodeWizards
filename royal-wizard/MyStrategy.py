from model.ActionType import ActionType
from model.Game import Game
from model.Move import Move
from model.Wizard import Wizard
from model.World import World

import random
from enum import Enum


class WizardState(Enum):
    Idle = 0
    GoToLane = 1
    Laning = 2
    Retreat = 3
    SwitchLane = 4
    Feed = 5 # LOL


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


class StateIdle(State):
    def __init__(self):
        super(StateIdle, self).__init__()
        pass

    def run(self, input):
        print("StateIdle")
        pass

    def next(self, input):
        return StateMachine.Idle


class StateGoToLane(State):
    def __init__(self):
        super(StateGoToLane, self).__init__()
        pass

    def run(self, input):
        print("StateGoToLane")
        self.forward_speed = 100
        self.turn_angle = random.randrange(30) - 15

    def next(self, input):
        if input["me"].y < 800:
            return StateMachine.Laning
        else:
            return StateMachine.GoToLane


class StateLaning(State):
    def __init__(self):
        super(StateLaning, self).__init__()
        pass

    def run(self, input):
        print("StateLaning")
        self.forward_speed = 0
        self.action = ActionType.MAGIC_MISSILE
        self.turn_angle = random.randrange(50) - 25
        pass

    def next(self, input):
        return StateMachine.Laning


class StateRetreat(State):
    def __init__(self):
        super(StateRetreat, self).__init__()
        pass

    def run(self, input):
        print("StateRetreat")
        pass

    def next(self, input):
        return StateMachine.Retreat


class StateSwitchLane(State):
    def __init__(self):
        super(StateSwitchLane, self).__init__()
        pass

    def run(self, input):
        print("StateSwitchLane")
        pass

    def next(self, input):
        return StateMachine.SwitchLane


class StateFeed(State):
    def __init__(self):
        super(StateFeed, self).__init__()
        pass

    def run(self, input):
        print("StateFeed")
        pass

    def next(self, input):
        return StateMachine.Feed


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


StateMachine.Idle = StateIdle()
StateMachine.GoToLane = StateGoToLane()
StateMachine.Laning = StateLaning()
StateMachine.Retreat = StateRetreat()
StateMachine.SwitchLane = StateSwitchLane()
StateMachine.Feed = StateFeed()

state_machine = StateMachine(initial_state=StateMachine.GoToLane)


class MyStrategy:
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
