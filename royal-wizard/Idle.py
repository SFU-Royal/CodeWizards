from Common import (State,
                    StateMachine)


class StateIdle(State):
    def __init__(self):
        super(StateIdle, self).__init__()
        pass

    def run(self, input_dict):
        print("StateIdle")
        pass

    def next(self, input_dict):
        return StateMachine.Idle
