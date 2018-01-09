"""
   use simpy simulate Pascal's triangle

1
23
456
"""
from simpy import Environment, FilterStore
from collections import namedtuple


WAIT_TIME = 10

class Port(object):

    def __init__(self,env,layer,num,next_ports,isleaf):
        self.layer  = layer
        self.num = num
        self.next_ports = FilterStore(env,capacity=2)
        self.next_ports.items = next_ports
        self.isleaf = isleaf
        if self.isleaf:
            self.end_num = 0


def go_next(env,user,startport):
    if startport.isleaf:
        startport.end_num += 1
        print('{user} reach leaf {num}'.format(user=user,num=startport.num))
    else:
        next_port = yield startport.next_ports.get()
        yield env.timeout(WAIT_TIME)
        print('{user} from {startport} to {port_name} at {time}'.format(
            user=user,
            startport=startport.num,
            port_name=next_port.num,time=env.now
        )
        )
        startport.next_ports.put(next_port)
        env.process(go_next(env,user,next_port))


if __name__ == '__main__':
    env = Environment()
    p4,p5,p6 = tuple(Port(env,3,i+4,[],True) for i in range(3))
    p2  = Port(env,2,2,[p6,p5],False)
    p3  = Port(env,2,3,[p4,p5],False)
    p1  = Port(env,1,1,[p2,p3],False)
    for i in range(1000):
        print(i)
        env.process(go_next(env,i,p1))
    env.run()
    print(p4.end_num,p5.end_num,p6.end_num)
