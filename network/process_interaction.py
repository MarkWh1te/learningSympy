"""
 simpy tutorial process interaction part
"""
from simpy import Environment, Interrupt


class Car(object):
    def __init__(self,env):
        self.env = env
        self.action = env.process(self.run())

    def run(self):
        while 1:
            print('start at %d' % self.env.now )
            try:
                charge_time = 5
                yield self.env.process(self.charge(charge_time))
            except Interrupt:
                 # When we received an interrupt, we stop charging and
                 # switch to the "driving" state
                 print('Was interrupted. Hope, the battery is full enough')

            print('start drive at %d' % self.env.now)
            trip_time = 2
            yield self.env.timeout(trip_time)

    def charge(self,charge_time):
        print('start charge %d' % self.env.now)
        yield self.env.timeout(charge_time)

def drive(env, car):
    yield env.timeout(3)
    car.action.interrupt()


if __name__ == '__main__':
    env = Environment()
    car = Car(env)
    env.process(drive(env, car))
    env.run(until=15)
