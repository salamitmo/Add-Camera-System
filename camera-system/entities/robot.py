class Robot:

    def __init__(self, x=0, y=0, z=0):

        self.position = [x, y, z]

    def get_position(self):
        return self.position