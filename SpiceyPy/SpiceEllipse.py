__author__ = 'Apollo117'


class Ellipse(object):
    """Class representing the C struct SpiceEllipse"""
    def __init__(self, center=None, semi_major=None, semi_minor=None):
        self.center = center or [0.0] * 3
        self.semi_major = semi_major or [0.0] * 3
        self.semi_minor = semi_minor or [0.0] * 3

    def __repr__(self):
        return '<SpiceEllipse: center = %s, semi_major = %s, semi_minor = %s>' % \
            (self.center, self.semi_major, self.semi_minor)