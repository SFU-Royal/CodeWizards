from Common import (State,
                    StateMachine)


class StateSwitchLane(State):
    def __init__(self):
        super(StateSwitchLane, self).__init__()
        pass

    def run(self, input_dict):
        print("StateSwitchLane")
        pass

    def next(self, input_dict):
        return StateMachine.SwitchLane
