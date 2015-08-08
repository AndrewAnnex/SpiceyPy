__author__ = 'AndrewAnnex'

__all__ = ['wrapper']

from spiceypy.wrapper import *

#Default setting for error reporting so that programs don't just exit out!
erract("set", 10, "return")
errdev("set", 10, "null")