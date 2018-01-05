from finangler import FinAngler
import numpy as np

if __name__ == '__main__':
    s = FinAngler()

    # Test forces_to_angles
    a = [0,0,.3]
    print s.forces_to_angles(a)

    # Test timing for calc_angles    
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

