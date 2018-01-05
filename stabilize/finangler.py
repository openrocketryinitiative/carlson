import numpy as np

'''
given the roll and pitch of the rocket, generates commands to be applied to the 
servos to stabilize the rockets attitude
'''
class FinAngler():
    def __init__(self):
        self.fin_angles = [0, 120, 240] # a list of the fins angles in degress
        self.fin_angles = np.array(self.fin_angles) / 180. * np.pi
        self.velocity = 1 #estimated velocity of the rocket in m/s

    # takes in a desired force to be applied to the rocket and find the 
    # appropriate fin angles to generate that force
    # - angle: the dirction in which to apply the force
    # - force: the magnitude of the force to be applied
    # - spin: the amount of yaw force around the long axis to be applied
    def calc_angles(self, angle, force, spin):
        # the component of each fins force that contributes to the desired force
        in_components  = np.sin(self.fin_angles - (angle/180. * np.pi))     
        in_components  = in_components/np.linalg.norm(in_components)
        # the component of each fins force that is out of axis with the desired force
        out_components = np.cos(self.fin_angles - (angle/180. * np.pi))     
        out_components = out_components/np.linalg.norm(out_components)
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
        return np.arcsin(forces/(self.velocity**2)) / np.pi * 180.


if __name__ == '__main__':
    s = FinAngler()

    N_ITERS = 10000

    ANGLE =  0
    FORCE =  0
    SPIN  = -2

    # Timing test
    from time import time
    times = []
    for i in range(N_ITERS):
        start = time()
        s.calc_angles(ANGLE, FORCE, SPIN)
        stop = time()
        times.append(stop - start)

    print "Average time for calc_angles: %0.8f seconds" % np.mean(np.array(times))

    # print '\nDEMO SPIN'
    # for i in range(-3,4):
    #   print 'Desired spin: {:1.2f}\t fin angles: {}'.format(i/3., s.calc_angles(0,0,i/3.))
    # print '\nDEMO FORCE ANGLE'
    # for i in range(0,7):
    #   print 'Desired angle: {}\t fin angles: {}'.format(i/3. * 180., s.calc_angles(i/3.*180.,1.,0))
    # print '\nDEMO FORCE'
    # for i in range(-3,4):
    #   print 'Desired force: {:1.2f}\t fin angles: {}'.format(i/3., s.calc_angles(0,-i/3.,0))