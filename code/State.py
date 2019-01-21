class State:
    def __init__(self, name=None):
        self.name = str(name)

    def __repr__(self):
        return 'State(' + self.name + ")"