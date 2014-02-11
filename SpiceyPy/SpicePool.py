__author__ = 'Apollo117'
from collections import UserDict


class SpicePool(UserDict):

    def clpool(self):
        """
        Clear the pool of kernel variables

        """
        pass

    def cvpool(self, agent, update):
        """
        Check variable in the pool for update

        """
        pass

    def dtpool(self, name, found, n, typeParam):
        """
        Data for a kernel pool variable
        :param name:
        :param found:
        :param n:
        :param typeParam:
        """
        pass

    def dvpool(self, name):
        """
        Delete a variable from the kernel pool

        """
        pass

    def expool(self, name):
        """
        Confirm the existence of a pool kernel variable

        """
        pass

    def furnsh(self, file):
        """
        Furnish a program with SPICE kernels
        :param file:
        """
        pass

    def gcpool(self, name, start, room, n, cvals, found):
        """
        Get character data from the kernel pool
        :param name:
        :param start:
        :param room:
        :param n:
        :param cvals:
        :param found:
        """
        pass

    def gdpool(self, name, start, room, n, values, found):
        """
        Get d.p. values from the kernel pool
        :param name:
        :param start:
        :param room:
        :param n:
        :param values:
        :param found:
        """
        pass

    def getfov(self, instid, room, shape, frame, bsight, n, bounds):
        """
        Fetch instrument FOV configuration
        :param instid:
        :param room:
        :param shape:
        :param frame:
        :param bsight:
        :param n:
        :param bounds:
        """
        pass

    def gipool(self, name, start, room, n, ivals, found):
        """
        Get integers from the kernel pool
        :param start:
        :param room:
        :param n:
        :param ivals:
        :param found:
        """
        pass

    def gnpool(self, name, start, room, n, cvals, found):
        """
        Get names of kernel pool variables
        :param name:
        :param start:
        :param room:
        :param n:
        :param cvals:
        :param found:
        """
        pass

    def kdata(self, which, kind, file, filtyp, source, handle, found):
        #Determine if a kernel pool variable is present and if so that it has the correct size and type.
        """

        :param which:
        :param kind:
        :param file:
        :param filtyp:
        :param source:
        :param handle:
        :param found:
        """
        pass

    def kinfo(self, file, filtyp, source, handle, found):
        #Return information about a loaded kernel specified by name.
        """

        :param file:
        :param filtyp:
        :param source:
        :param handle:
        :param found:
        """
        pass

    def ktotal(self, kind, count):
        #Return the current number of kernels that have been loaded via the KEEPER
        # interface that are of a specified type.
        """

        :param kind:
        :param count:
        """
        pass

    def ldpool(self, kernel):
        """
        Load variables from a kernel file into the pool
        :param kernel:
        """
        pass

    def lmpool(self, cvals, n):
        """
        Load variables from memory into the pool
        :param cvals:
        :param n:
        """
        pass

    def pcpool(self, name, n, cvals):
        """
        Put character strings into the kernel pool
        :param name:
        :param n:
        :param cvals:
        """
        pass

    def pdpool(self, name, n, values):
        """
        Put d.p.'s into the kernel pool
        :param name:
        :param n:
        :param values:
        """
        pass

    def pipool(self, name, n, ivals):
        """
        Put integers into the kernel pool
        :param name:
        :param n:
        :param ivals:
        """
        pass

    def stpool(self, item, nth, contin, string, size, found):
        """
        String from pool
        :param item:
        :param nth:
        :param contin:
        :param string:
        :param size:
        :param found:
        """
        pass

    def swpool(self, agent, nnames, names):
        """
        Set watch on a pool variable
        :param agent:
        :param nnames:
        :param names:
        """
        pass

    def szpool(self, name, n, found):
        """
        Get size limitations of the kernel pool
        :param name:
        :param n:
        :param found:
        """
        pass

    def unload(self, file):
        """
        Unload a kernel
        :param file:
        """
        pass