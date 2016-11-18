from Common import (State,
                    StateMachine)


class StateDead(State):
    def __init__(self):
        super(StateDead, self).__init__()
        pass

    def run(self, input_dict):
        print("StateDead")
        pass

    def next(self, input_dict):
        return StateMachine.Dead
