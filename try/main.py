from db import query
from path import taxi_graph_1, drive_graph
from config import AIR_LIST
from entity import Aircraft, nodes

import simpy,time


env = simpy.Environment()

aircrafts = query("select * from aircraft")

Time = -46200
node_res = nodes(taxi_graph_1, env, simpy.Resource)

for i in aircrafts:
	air = Aircraft(env, node_res, i)
	AIR_LIST.append(air)


env.run()
x = 0

for i in AIR_LIST:
	# if i.aircraft_id == '5':
	# 	print(i.plan_time)
	# 	print(i.ccc)
	x += i.conflict_time
print(x)
print(x/60)

# def a(aircrafts):
# 	x = Time
# 	for aircraft in aircrafts:
# 		air = Aircraft(aircraft)
# 		y = air.landing_time
# 		time.sleep(2)
# 		yield env.timeout(y-x)
# 		x = y
# 		print('%s park success at %d' % (air.aircraft_id, env.now))
#
# env.process(a(aircrafts))
# env.run()
# a = Aircraft(aircrafts[0])
# print(a.time)
# print(taxi_graph_1.edges[('R-5', 'D-9')]['length'])
