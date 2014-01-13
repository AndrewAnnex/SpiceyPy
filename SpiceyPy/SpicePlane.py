__author__ = 'Apollo117'


class Plane(object):
    def __init__(self, normal=[0.0]*3, constant=0.0):
        self.normal = normal
        self.constant = constant

    def __str__(self):
        return '<Plane: normal=%s; constant=%s>' % (', '.join([str(x) for x in self.normal]), self.constant)