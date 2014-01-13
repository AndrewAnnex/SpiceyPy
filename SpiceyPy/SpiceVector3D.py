__author__ = 'Apollo117'
import copy


class SpiceVector3D(object):

    def __init__(self, x=None, y=None, z=None, xyz=None):
        if x is None and y is None and z is None and xyz is None:
            self._xyz = self.defaultXYZ()
            self._x = self._xyz[0]
            self._y = self._xyz[1]
            self._z = self._xyz[2]
        if xyz is None:
            self._x = x
            self._y = y
            self._z = z
            self.xyz = (self._x, self._y, self._z)
        else:
            self._xyz = xyz
            self._x = self._xyz[0]
            self._y = self._xyz[1]
            self._z = self._xyz[2]

    @property
    def x(self):
        return self._x or self.defaultX()

    @x.setter
    def x(self, value):
        self._x = value
        self._update()

    @property
    def y(self):
        return self._y or self.defaultY()

    @y.setter
    def y(self, value):
        self._y = value
        self._update()

    @property
    def z(self):
        return self._z or self.defaultZ()

    @z.setter
    def z(self, value):
        self._z = value
        self._update()

    @property
    def xyz(self):
        return self._xyz or self.defaultXYZ()

    @xyz.setter
    def xyz(self, value):
        self._xyz = value
        self.x = value[0]
        self.y = value[1]
        self.z = value[2]

    def _update(self):
        self.xyz = (self._x, self._y, self._z)

    def defaultX(self):
        return 0.0

    def defaultY(self):
        return 0.0

    def defaultZ(self):
        return 0.0

    def defaultXYZ(self):
        return (0.0, 0.0, 0.0)

    def copy(self):
        return copy.deepcopy(self)

    def __repr__(self):
        keys = sorted(self.__dict__, key=len)
        items = ("{}={!r}".format(k, self.__dict__[k]) for k in keys)
        return "{}({})".format(type(self).__name__, ", ".join(items))







def test():
    xyz = (1, 2, 3)
    x=1
    y=2
    z=3
    a = SpiceVector3D(xyz=xyz)
    c = SpiceVector3D()
    print(c)
    print(a.xyz)
    b = a.copy()
    b.xyz = (51,1,1)
    print(b.xyz)
    print(a.xyz)
    print(type(a))
    print(a)

test()


