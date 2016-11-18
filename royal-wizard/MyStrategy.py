from model.ActionType import ActionType
from model.Game import Game
from model.Move import Move
from model.Wizard import Wizard
from model.World import World
from model.LaneType import LaneType
from model.Message import Message
from model.Faction import Faction

import random
from enum import Enum


PATH_FINDING_EPS = 10.0


class WizardState(Enum):
    Idle = 0
    GoToLane = 1
    Laning = 2
    Retreat = 3
    SwitchLane = 4
    Feed = 5 # LOL
    Dead = 6


class KeyPoint():
    def __init__(self, x, y):
        self.x = x;
        self.y = y


def get_nearest_visiable_enemy(me, minions, wizards, include_neutral=False):
    nearest_enemy = None
    shortest_dist = 100000

    enemy_faction = [1 - me.faction]
    if include_neutral:
        enemy_faction.append[Faction.NEUTRAL]

    for minion in minions:
        if minion.faction in enemy_faction:
            if me.get_distance_to(minion.x, minion.y) < shortest_dist:
                shortest_dist = me.get_distance_to(minion.x, minion.y)
                nearest_enemy = minion
    for wizard in wizards:
        if wizard.faction in enemy_faction:
            if me.get_distance_to(wizard.x, wizard.y) < shortest_dist:
                shortest_dist = me.get_distance_to(wizard.x, wizard.y)
                nearest_enemy = wizard
    return nearest_enemy


class LaneKeyPoints():
    def __init__(self):
        self.keypoints = [[], [], []]

    def update_keypoints(self, lane, keypoints):
        self.keypoints[lane] = keypoints

    def get_lane_keypoints(self, lane = LaneType.TOP):
        return self.keypoints[lane];


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


class StateLaning(State):
    def __init__(self):
        super(StateLaning, self).__init__()
        pass

    def run(self, input):
        print("StateLaning")
        me = input["me"]
        world = input["world"]
        minions = world.minions
        wizards = world.wizards
        nearest_enemy = get_nearest_visiable_enemy(me, minions, wizards)
        # TODO: the right way to lancing
        self.forward_speed = 0
        self.action = ActionType.MAGIC_MISSILE
        if nearest_enemy is not None:
            self.turn_angle = me.get_angle_to(nearest_enemy.x, nearest_enemy.y)
        else:
            self.turn_angle = 0

    def next(self, input):
        me = input["me"]
        world = input["world"]
        minions = world.minions
        wizards = world.wizards
        nearest_enemy = get_nearest_visiable_enemy(me, minions, wizards)
        # TODO: a better check for retreat
        if nearest_enemy is None:
            return StateMachine.GoToLane
        elif me.life < me.max_life * 0.25:
            return StateMachine.Retreat
        else:
            return StateMachine.Laning


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


class StateDead(State):
    def __init__(self):
        super(StateDead, self).__init__()
        pass

    def run(self, input):
        print("StateDead")
        pass

    def next(self, input):
        return StateMachine.Dead


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

StateMachine.Idle = StateIdle()
StateMachine.GoToLane = StateGoToLane()
StateMachine.Laning = StateLaning()
StateMachine.Retreat = StateRetreat()
StateMachine.SwitchLane = StateSwitchLane()
StateMachine.Feed = StateFeed()
StateMachine.Dead = StateDead()

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
