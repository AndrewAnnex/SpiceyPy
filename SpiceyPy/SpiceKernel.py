__author__ = 'Apollo117'

import struct


class SpiceKernel(object):

    def __init__(self):
        pass

    def open(self, fileP):
        with open(fileP, "rb") as f:
            self.locidw = b''.join(struct.unpack('c' * 8, f.read(8)))
            self.nd = struct.unpack('i', f.read(4))[0]
            self.ni = struct.unpack('i', f.read(4))[0]
            self.LOCIFN = b''.join(struct.unpack('c' * 60, f.read(60)))
            self.FWARD = struct.unpack('i', f.read(4))[0]
            self.BWARD = struct.unpack('i', f.read(4))[0]
            self.FREE = struct.unpack('i', f.read(4))[0]
            self.LOCFMT = b''.join(struct.unpack('c' * 8, f.read(8)))
            self.PRENUL = struct.unpack('c' * 603, f.read(603))
            self.FTPSTR = b''.join(struct.unpack('c' * 28, f.read(28)))
            self.PSTNUL = struct.unpack('c' * 297, f.read(297))