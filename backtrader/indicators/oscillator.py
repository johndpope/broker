#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys

import six

from . import Indicator, MovingAverage


class OscillatorMixIn(Indicator):
    '''
    MixIn class to create a subclass with another indicator. The main line of
    that indicator will be substracted from the other base class main line
    creating and oscillator

    The usage is:

      - Class XXXOscillator(XXX, OscillatorMixIn)

    Formula:
      - XXX calculates lines[0]
      - osc = self.data - XXX.lines[0]
    '''
    plotlines = dict(_0=dict(_name='osc'))

    def _plotinit(self):
        try:
            lname = self.lines._getlinealias(0)
            self.plotlines._0._name = lname + '_osc'
        except AttributeError:
            pass

    def __init__(self):
        self.lines[0] = self.data - self.lines[0]
        super(OscillatorMixIn, self).__init__()


class Oscillator(Indicator):
    '''
    Oscillation of a given data around another data

    Datas:
      This indicator can accept 1 or 2 datas for the calculation.

      - If 1 data is provided, it must be a complex "Lines" object (indicator)
        which also has "datas". Example: A moving average

        The calculated oscillation will be that of the Moving Average (in the
        example) around the data that was used for the average calculation

      - If 2 datas are provided the calculated oscillation will be that of the
        2nd data around the 1st data

    Formula:
      - 1 data -> osc = data.data - data
      - 2 datas -> osc = data0 - data1
    '''
    lines = ('osc',)

    # Have a default value which can be later modified if needed
    plotlines = dict(_0=dict(_name='osc'))

    def _plotinit(self):
        try:
            lname = self.dataosc._getlinealias(0)
            self.plotlines._0._name = lname + '_osc'
        except AttributeError:
            pass

    def __init__(self):
        super(Oscillator, self).__init__()

        if len(self.datas) > 1:
            datasrc = self.data
            self.dataosc = self.data1
        else:
            datasrc = self.data.data
            self.dataosc = self.data

            self.lines[0] = datasrc - self.dataosc


# Automatic creation of Oscillating Lines

for movav in MovingAverage._movavs[1:]:
    _newclsdoc = '''
    Oscillation of a %s around its data
    '''
    # Skip aliases - they will be created automatically
    if getattr(movav, 'aliased', ''):
        continue

    movname = movav.__name__
    linename = movav.lines._getlinealias(0)
    newclsname = movname + 'Oscillator'

    newaliases = [movname + 'Osc']
    for alias in getattr(movav, 'alias', []):
        for suffix in ['Oscillator', 'Osc']:
            newaliases.append(alias + suffix)

    newclsdoc = _newclsdoc % movname
    newclsdct = {'__doc__': newclsdoc,
                 '__module__': OscillatorMixIn.__module__,
                 '_notregister': True,
                 'alias': newaliases}

    newcls = type(str(newclsname), (movav, OscillatorMixIn), newclsdct)
    module = sys.modules[OscillatorMixIn.__module__]
    setattr(module, newclsname, newcls)
