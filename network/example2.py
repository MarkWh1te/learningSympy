import simpy
from SimComponents import PacketGenerator, PacketSink, SwitchPort

def constArrival():
    return 1.5    # time interval

def constSize():
    return 100.0  # bytes

env = simpy.Environment()  # Create the SimPy environment
ps = PacketSink(env, debug=True) # debug: every packet arrival is printed
pg = PacketGenerator(env, "SJSU", constArrival, constSize)
switch_port = SwitchPort(env, rate=200.0, qlimit=300)
# Wire packet generators and sinks together
pg.out = switch_port
switch_port.out = ps
env.run(until=20)
print("waits: {}".format(ps.waits))
print("received: {}, dropped {}, sent {}".format(ps.packets_rec,
     switch_port.packets_drop, pg.packets_sent))
