"""
 simpy tutorial process interaction part
"""
from simpy import Environment, Resource


def car(env, name, bcs, driving_time, charge_duration):
    "battery charging station (BCS) is bsc resource "
    yield env.timeout(driving_time)
    print("{name} arrive at battery charging station at {time}".format(name=name,time=env.now))
    with bcs.request() as req:
        yield req
        print('%s starting to charge at %s' % (name, env.now))
        yield env.timeout(charge_duration)
        print('%s leaving the bcs at %s' % (name, env.now))

if __name__ == '__main__':
    env = Environment()
    bcs = Resource(env, capacity=2)
    for i in range(4):
        env.process(car(env, 'Car {num}'.format(num=str(i)),bcs,i*2,5))
    env.run()
