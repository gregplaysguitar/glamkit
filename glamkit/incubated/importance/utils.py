from __future__ import division
import datetime

from django.db import models

def calculate_importance(spikes, max_importance, min_importance, tenthlife, importance_field="importance"):
    def wrapper(cls):
        fields = [f.name for f in cls._meta.fields]
        def check(dat):
            if not dat in fields:
                raise DateCalculatorException("Class '%s' does not have a '%s' attribute, though it is specified in the @calculate_importance decorator" % (cls.__name__, dat))
        for dat in spikes:
            if isinstance(dat, tuple):
                map(check, dat)
            else:
                check(dat)
        cls.importance_field = importance_field
        cls.calculate_importance = lambda self: DateCalculator(self, tenthlife, max_importance, min_importance, spikes).get_importance()
        return cls
    return wrapper

class DateCalculator(object):
    """
    calculate the importance for the object based on the current time
    """
    def _resolve(self, dat):
        return getattr(self.obj, dat)
        
    def _smart_resolve(self, dat):
        if isinstance(dat, tuple):
            return map(self._resolve, dat)
        else:
            return self._resolve(dat)
        
    def _calculate(self, closest):
        return max(self.min_importance, self.max_importance / 10 ** (abs(self.now-closest).days / self.tenthlife))
        
    def __init__(self, obj, tenthlife, max_importance, min_importance, spike_list):
        self.obj = obj
        self.max_importance = max_importance
        self.min_importance = min_importance
        self.tenthlife = tenthlife
        
        self.spike_list = spike_list
        
    def _resolve_everything(self):
        spike_list = map(self._smart_resolve, self.spike_list)
        
        self.spikes = []
        self.max_periods = []
        for dat in spike_list:
            if isinstance(dat, tuple):
                if len(dat) == 2:
                    self.max_periods.append(dat)
                    start, finish = dat
                    self.spikes.append(start)
                    self.spikes.append(finish)
                else:
                    self.spikes.append(dat[0])
                    self.max_periods.append((dat[0], datetime.date.max))
            else:
                self.spikes.append(dat)
        self.spikes.sort()
        
    def get_importance(self):
        self._resolve_everything()
        
        max_spike = max(self.spikes)
        min_spike = min(self.spikes)
        self.now = datetime.date.today()
        
        for start, finish in self.max_periods:
            if start <= self.now <= finish:
                return self.max_importance
        if self.now >= max_spike:
            return self._calculate(max_spike)
        elif self.now <= min_spike:
            return self._calculate(min_spike)
        else:
            for i, spike in enumerate(spikes):
                if spike >= self.now:
                    start, finish = spikes[i-1], spike
                    closest = start if self.now - start > finish - self.now else finish
                    return self._calculate(closest)         
                    
class DateCalculatorException(Exception):
    pass