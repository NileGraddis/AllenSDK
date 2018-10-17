from collections import namedtuple

import numpy as np

Key = namedtuple('Key', ('structure_id', 'hemisphere_id', 'injection', 'name'))


class Field(object):
    
    __slots__ = ('value',)

    @property
    def required_intervals(self):
        return []
    

    @property
    def required_fields(self):
        return {}


    def __init__(self, key, **data):
        self.key = Key(*key)
        self.__dict__.update(data)

    
    def calculate(self, low=None, high=None, **inputs):
        raise NotImplementedError


    @classmethod
    def propagate(cls, key, inputs):
        raise NotImplementedError


class SumPixelsField(Field):

    @property
    def required_intervals(self):
        response = ['sum_pixels', 'injection_fraction']
        if not self.key.injection:
            response.append('aav_exclusion_fraction')
        return response


    @property
    def required_fields(self):
        if not self.key.injection:
            return {'injection_sum_pixels_field': Key(self.key.structure_id, self.key.hemisphere_id, True, self.key.name)}
        return {}


    def calculate(self, low, high, **data):
        if self.key.injection:
            self.value = np.multiply(data['sum_pixels'][low:high], data['injection_fraction'][low:high]).sum()

        else:
            nex = np.logical_or(data['injection_fraction'][low:high], np.logical_not(data['aav_exclusion_fraction'][low:high]))
            self.value = data['sum_pixels'][low:high][nex].sum() 
            self.value -= data['injection_sum_pixels_field'].value


    @classmethod
    def propagate(cls, key, inputs):
        return cls(key, value=sum(inp.value for inp in inputs))


class SumProjectingPixelsField(Field):

    @property
    def required_intervals(self):
        if self.key.injection:
            return ['sum_pixels', 'injection_density']
        else:
            return ['sum_pixels', 'projection_density', 'aav_exclusion_fraction', 'injection_fraction']


    @property
    def required_fields(self):
        if not self.key.injection:
            return {'injection_sum_projecting_pixels_field': Key(self.key.structure_id, self.key.hemisphere_id, True, self.key.name)}


    def calculate(self, low, high, **data):
        if self.key.injection:
            self.value = np.multiply(data['sum_pixels'][low:high], data['injection_density'][low:high]).sum()
        else:
            nex = np.logical_or(data['injection_fraction'][low:high], np.logical_not(data['aav_exclusion_fraction'][low:high]))
            self.value = np.multiply(data['sum_pixels'][low:high], data['projection_density'][low:high]).sum()
            self.value -= data['injection_sum_projecting_pixels_field'].value

    @classmethod
    def propagate(cls, key, inputs):
        return cls(key, value=sum(inp.value for inp in inputs))


class ProjectionDensityField(Field):

    @property
    def required_fields(self):
        return {
            'sum_pixels_field': Key(self.key.structure_id, self.key.hemisphere_id, self.key.injection, 'sum_pixels'), 
            'sum_projecting_pixels_field': Key(self.key.structure_id, self.key.hemisphere_id, self.key.injection, 'sum_projecting_pixels')
        }


    def calculate(self, low=None, high=None, **data):
        self.value = data['sum_projection_pixels_field'].value / data['sum_pixels_field'].value