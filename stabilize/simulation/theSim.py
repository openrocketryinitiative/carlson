from math import pi, sin, cos
import numpy as np
from components import components
import time
import matplotlib.pyplot as plt
from matplotlib import animation 

class E2:
    def __init__(self, x,y,theta):
        self.x = x
        self.y = y
        self.theta = theta

    def get_state(self):
        return np.array([self.x,self.y,self.theta])

class Fluid:
    def __init__(self, density):
        self.density = density

    def drag(self, frontal_area, drag_coeff, velocity):
        return drag_coeff * frontal_area * velocity ** 2 * self.density / 2.

    def lift(self, frontal_area, lift_coeff, velocity):
        return lift_coeff * frontal_area * velocity ** 2 * self.density / 2.

class Rocket:
    def __init__(self, components):
        # for now approx lift/drag of entire rocket
        self.drag_coeff = .82
        self.lift_coeff = .6

        # air has density 1.225 kg/m^3
        self.fluid = Fluid(1.225)

        init_pos_x = 0.
        init_pos_y = 0.
        # initial angle of attack
        init_theta = np.radians(2)

        init_vel_x = 1.
        init_vel_y = 50.
        # initial rotation
        init_vel_theta = 0.

        self.position = E2(init_pos_x, init_pos_y, init_theta)
        self.velocity = E2(init_vel_x, init_vel_y, init_vel_theta)

        self.components = components
        self.mass = 0.
        cm_sum = 0.
        cg_sum = 0.
        area_sum = 0.
        for c in self.components:
            self.mass += c.mass
            cm_sum += c.abs_cm * c.mass
            cg_sum += c.abs_cg * c.area
            area_sum += c.area

        self.cm = cm_sum / self.mass
        self.cg = cg_sum / area_sum
        self.area = area_sum
        
        self.rotational_inertia = 0
        for c in self.components:
            self.rotational_inertia += c.rotational_inertia(self.cm)

        assert self.cg - self.cm >= 0., "unstable rocket"
        print self.cg - self.cm

    def step(self, dt):
        travel_direction = np.arctan2(self.velocity.x, self.velocity.y)
        aoa =  travel_direction - self.position.theta
        velocity2 = self.velocity.x**2 + self.velocity.y**2
        tot_lift = 0
        tot_drag = 0
        torque = 0

        for c in self.components:
            dist_to_cg = c.abs_cg - self.cg
            force = c.width * c.height * velocity2 * self.fluid.density / 2.

            drag = - (sin(aoa) + .03) * force * self.drag_coeff
            lift = (sin(aoa) * cos(aoa) * force * self.lift_coeff)

            rotational_drag = - np.sign(self.velocity.theta) *(self.velocity.theta * dist_to_cg)**2 * c.width * c.height * self.fluid.density / 2. * self.drag_coeff

            tot_lift += lift
            tot_drag += drag
            torque += (drag * sin(aoa) + lift * cos(aoa)) * abs(self.cg - self.cm) + 10. * rotational_drag


        acceleration_x = sin(travel_direction) * drag - cos(travel_direction) * lift
        acceleration_y = cos(travel_direction) * drag + sin(travel_direction) * lift
        
        self.velocity.x += acceleration_x * dt
        self.velocity.y += (acceleration_y - 9.81) * dt
        self.velocity.theta += torque/self.rotational_inertia * dt

        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt
        self.position.theta += self.velocity.theta * dt

if __name__ == '__main__':
    r = Rocket(components)
    ps = []
    vs = []
    ts = []
    start_time = time.time()
    t = 0
    tt = t
    time_multiple = 6.
    for i in range(40000):
        if r.position.y < 0:
            break

        t = time.time() - start_time
        ts.append(t*time_multiple)
        dt = (t - tt) * time_multiple
        r.step(dt)
        ps.append(r.position.get_state())
        vs.append(r.velocity.get_state())
        # print'%3f %3f %3f' % (r.velocity.x, r.velocity.y, r.position.theta)
        tt = t

    ps = np.array(ps)
    vs = np.array(vs)
    # plt.plot(ts, vs[:,0], label='$v_x$')
    # plt.plot(ts, vs[:,1], label='$v_y$')
    # plt.plot(ts, ps[:,1], label='$y$')
    plt.plot(ts, ps[:,2] % (2*pi), label='$\\theta$')
    plt.plot(ts, np.arctan2(vs[:,0], vs[:,1]), label="travel_direction")
    apogee = ts[np.argmin(np.absolute(vs[:,1]))]
    plt.axvline(x=apogee, label='')
    # plt.plot(ts[:-1], np.diff(vs[:,1])/(ts[:-1]), label='$a_y$')
    plt.legend()
    plt.show()
    plt.savefig('uh.png')
    plt.clf()

