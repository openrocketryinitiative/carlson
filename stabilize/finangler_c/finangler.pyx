import numpy as np
cimport numpy as np

'''
given the roll and pitch of the rocket, generates commands to be applied to the 
servos to stabilize the rockets attitude
'''
class FinAngler:

    DEF TO_DEG = 57.295779579
    DEF TO_RAD =  0.017453293

    def __init__(self):
        self.fin_angles = [0, 120, 240]  # a list of the fins angles in degress
        self.fin_angles = np.array(self.fin_angles) * TO_RAD
        self.velocity   = 1  # estimated velocity of the rocket in m/s

    # Return normal of ndarray `v`.
    def norm(self, v):
        cdef double inner_sum
        inner_sum = 0
        if type(v) is list:
            v = np.array(v)
        for i in range(v.size):
            inner_sum = inner_sum + (v[i] ** 2)
        return np.sqrt(inner_sum)

    # takes in a desired force to be applied to the rocket and find the 
    # appropriate fin angles to generate that force
    # - angle: the dirction in which to apply the force
    # - force: the magnitude of the force to be applied
    # - spin: the amount of yaw force around the long axis to be applied
    def calc_angles(self, angle, force, spin):

        # the component of each fins force that contributes to the desired force
        in_components  = np.sin(self.fin_angles - (angle * TO_RAD))
        in_components  = in_components / self.norm(in_components)

        # the component of each fins force that is out of axis with the desired force
        out_components = np.cos(self.fin_angles - (angle * TO_RAD))
        out_components = out_components / self.norm(out_components)

        # generate a 3x3 matrix where the rows are the components and ones
        effects_matrix = np.stack((in_components, out_components, np.ones(in_components.shape)))
        results_matrix = np.array([force, 0, spin]).T

        # effects * forces = results
        fin_forces = np.linalg.lstsq(effects_matrix,results_matrix)

        return self.forces_to_angles(fin_forces[0])

    # takes an array of fin forces and returns an array of fin angles
    # to generate those forces. This will need to be updated with
    # a more advanced model incorporating fin AOA in the future
    def forces_to_angles(self, forces):
        new_forces = np.array([0,0,0])
        # Convert to ndarray if of type list
        if type(forces) is list:
            forces = np.array(forces)
        for i in range(forces.size):
            new_forces[i] = np.arcsin(forces[i] / (self.velocity**2)) * TO_DEG
        return new_forces