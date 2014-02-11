__author__ = 'Apollo117'
# Collection of Constants for Spice
import numpy


def b1900():
    #Return the Julian Date corresponding to Besselian Date 1900.0.
    """


    :return:
    """
    return 2415020.31352


def b1950():
    #Return the Julian Date corresponding to Besselian Date 1950.0.
    """


    :return:
    """
    return 2433282.42345905


def clight():
    #Return the speed of light in a vacuum (IAU official value, in km/sec)
    """


    :return:
    """
    return 299792.458


def dpr():
    return 180.0 / numpy.pi


def halfpi():
    return numpy.pi / 2


def j1900():
    """
    :rtype : float
    :return: the Julian Date of 1899 DEC 31 12:00:00 (1900 JAN 0.5)
    """
    return 2415020.0


def j1950():
    """
    Return the Julian Date of 1950 JAN 01 00:00:00 (1950 JAN 1.0)

    :rtype : float
    :return: Julian Date of 1950 JAN 01 00:00:00 (1950 JAN 1.0)
    """
    return 2433282.5


def j2000():
    #Return the Julian Date of 2000 JAN 01 12:00:00 (2000 JAN 1.5)
    """

    :rtype : float
    :return: Julian Date of 2000 JAN 01 12:00:00 (2000 JAN 1.5)
    """
    return 2451545.0


def j2100():
    #Return the Julian Date of 2100 JAN 01 12:00:00 (2100 JAN 1.5)
    """

    :rtype : float
    :return: Julian Date of 2100 JAN 01 12:00:00 (2100 JAN 1.5)
    """
    return 2488070.0


def jyear():
    #Return the number of seconds in a julian year.
    """

    :rtype : float
    :return: the number of seconds in a julian year
    """
    return 31557600.0


def pi():
    return numpy.pi


def rpd():
    #Return the number of radians per degree.
    return numpy.pi / 180.0


def spd():
    #Return the number of seconds in a day.
    return 86400.0


def twopi():
    #Return twice the value of pi (the ratio of the circumference of a circle to its diameter)
    return numpy.pi * 2


def tyear():
    #Return the number of seconds in a tropical year.
    return 31556925.9747
