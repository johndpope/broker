#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from . import Indicator, Max, MovAv


class UpDay(Indicator):
    '''
    Defined by J. Welles Wilder, Jr. in 1978 in his book *"New Concepts in
    Technical Trading Systems"* for the RSI

    Recods days which have been "up", i.e.: the close price has been
    higher than the day before.

    Formula:
      - upday = max(close - close_prev, 0)

    See:
      - http://en.wikipedia.org/wiki/Relative_strength_index
    '''
    lines = ('upday',)

    def __init__(self):
        self.lines.upday = Max(self.data - self.data(-1), 0.0)
        super(UpDay, self).__init__()


class DownDay(Indicator):
    '''
    Defined by J. Welles Wilder, Jr. in 1978 in his book *"New Concepts in
    Technical Trading Systems"* for the RSI

    Recods days which have been "down", i.e.: the close price has been
    lower than the day before.

    Formula:
      - downday = max(close_prev - close, 0)

    See:
      - http://en.wikipedia.org/wiki/Relative_strength_index
    '''
    lines = ('downday',)

    def __init__(self):
        self.lines.downday = Max(self.data(-1) - self.data, 0.0)
        super(DownDay, self).__init__()


class UpDayBool(Indicator):
    '''
    Defined by J. Welles Wilder, Jr. in 1978 in his book *"New Concepts in
    Technical Trading Systems"* for the RSI

    Recods days which have been "up", i.e.: the close price has been
    higher than the day before.

    Note:
      - This version returns a bool rather than the difference

    Formula:
      - upday = close > close_prev

    See:
      - http://en.wikipedia.org/wiki/Relative_strength_index
    '''
    lines = ('upday',)

    def __init__(self):
        self.lines.upday = self.data > self.data(-1)
        super(UpDayBool, self).__init__()


class DownDayBool(Indicator):
    '''
    Defined by J. Welles Wilder, Jr. in 1978 in his book *"New Concepts in
    Technical Trading Systems"* for the RSI

    Recods days which have been "down", i.e.: the close price has been
    lower than the day before.

    Note:
      - This version returns a bool rather than the difference

    Formula:
      - downday = close_prev > close

    See:
      - http://en.wikipedia.org/wiki/Relative_strength_index
    '''
    lines = ('downday',)

    def __init__(self):
        self.lines.downday = self.data(-1) > self.data
        super(DownDayBool, self).__init__()


class RelativeStrengthIndex(Indicator):
    '''
    Defined by J. Welles Wilder, Jr. in 1978 in his book *"New Concepts in
    Technical Trading Systems"*.

    It measures momentum by calculating the ration of higher closes and
    lower closes after having been smoothed by an average, normalizing
    the result between 0 and 100

    Formula:
      - up = upday(data)
      - down = downday(data)
      - maup = movingaverage(up, period)
      - madown = movingaverage(down, period)
      - rs = maup / madown
      - rsi = 100 - 100 / (1 + rs)

    The moving average used is the one originally defined by Wilder,
    the SmoothedMovingAverage

    See:
      - http://en.wikipedia.org/wiki/Relative_strength_index
    '''
    alias = ('RSI', 'RSI_SMMA', 'RSI_Wilder',)

    lines = ('rsi',)
    params = (('period', 14),
              ('movav', MovAv.Smoothed),
              ('upperband', 70.0),
              ('lowerband', 30.0))

    def _plotlabel(self):
        plabels = [self.p.period]
        plabels += [self.p.movav] * self.p.notdefault('movav')
        return plabels

    def _plotinit(self):
        self.plotinfo.plotyhlines = [self.p.upperband, self.p.lowerband]

    def __init__(self):
        upday = UpDay(self.data)
        downday = DownDay(self.data)
        maup = self.p.movav(upday, period=self.p.period)
        madown = self.p.movav(downday, period=self.p.period)
        rs = maup / madown
        self.lines.rsi = 100.0 - 100.0 / (1.0 + rs)
        super(RelativeStrengthIndex, self).__init__()


class RSI_SMA(Indicator):
    '''
    Uses a SimpleMovingAverage as described in Wikipedia and other soures

    See:
      - http://en.wikipedia.org/wiki/Relative_strength_index
    '''
    alias = ('RSI_Cutler',)

    params = (('movav', MovAv.Simple),)


class RSI_EMA(Indicator):
    '''
    Uses an ExponentialMovingAverage as described in Wikipedia

    See:
      - http://en.wikipedia.org/wiki/Relative_strength_index
    '''
    params = (('movav', MovAv.Exponential),)
