from abc import abstractmethod
import numpy as np
from math import sin, cos, pi

class RocketComponent(object):
    def __init__(self, position, width, height, mass, name=None):
        self.width = width
        self.height = height
        self.mass = mass
        self.position = position
        self.area = self.component_area()
        self.cg = self.component_centroid_y()
        self.cm = self.component_center_mass_y()
        self.abs_cg = self.cg + self.position
        self.abs_cm = self.cm + self.position
        self.name = name if name else "unnamed"

    @abstractmethod
    def component_area(self):
        e = "Component class must have area method"
        raise NotImplementedError(e)

    @abstractmethod
    def component_centroid_y(self):
        e = "Component class must have centroid_y method"
        raise NotImplementedError(e)

    @abstractmethod
    def component_center_mass_y(self):
        e = "Component class must have center_mass_y method"
        raise NotImplementedError(e)

    @abstractmethod
    def rotational_inertia(self, cg):
        e = "Component class must have rot inertia method"
        raise NotImplementedError(e)

    @abstractmethod
    def frontal_v_area(self, aoa):
        e = "Component class must have frontal_v_area method"
        raise NotImplementedError(e)

    @abstractmethod
    def frontal_v_area(self, aoa):
        e = "Component class must have frontal_h_area method"
        raise NotImplementedError(e)


class Rectangle(RocketComponent):
    def __init__(self, *args):
        super(Rectangle, self).__init__(*args)

    def component_area(self):
        return self.width * self.height

    def component_centroid_y(self):
        return self.height / 2.

    def component_center_mass_y(self):
        return self.height / 2.

    def rotational_inertia(self, cg):
        w = self.width
        h = self.height
        py = self.position
        coeff = 1./12. * self.mass
        term1 = 4 * h**2 + w**2
        term2 = 12. * cg**2 + 12. * h * py
        term3 = 12. * py**2 - 12 * cg * (h + 2*py)
        return coeff * (term1 + term2 + term3)

    def frontal_v_area(self, aoa):
        return self.area * sin(aoa)

    def frontal_h_area(self, aoa):
        return self.area * cos(aoa)

class RocketBody(Rectangle):
    def __init__(self):
        super(RocketBody, self).__init__(0, .038, .7, .2, "body")

    def __repr__(self):
        return '<rocket-component-%s>' % self.name

    def __str__(self):
        return 'component-%s' % self.name

class RocketFins(Rectangle):
    def __init__(self):
        super(RocketFins, self).__init__(.7, .15, .075, .06, "fins")

    def __repr__(self):
        return '<rocket-component-%s>' % self.name

    def __str__(self):
        return 'component-%s' % self.name

components = [RocketFins(), RocketBody()]
