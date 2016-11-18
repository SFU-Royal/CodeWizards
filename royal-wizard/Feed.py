from Common import (State,
                    StateMachine)


class StateFeed(State):
    def __init__(self):
        super(StateFeed, self).__init__()
        pass

    def run(self, input_dict):
        print("StateFeed")
        pass

    def next(self, input_dict):
        return StateMachine.Feed
