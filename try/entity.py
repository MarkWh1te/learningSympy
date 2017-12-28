from path import path, taxi_graph_1
from threading import Thread
from config import AIRCRAFT_SPEED_TAXI, GLOBAL_TIMER, SAFE_TIME, AIR_LIST


node_dict = {}

# 将每个可能经过的节点初始为 Simpy 的共享资源，并限制同时刻只能有一个对象占用资源
def nodes(G, env, Resource):
	res = {}
	for n in G.nodes:
		res[n] = Resource(env, capacity=1)
	return res


def take_resource(env, res):
	print(1)
	with res.request() as req:
		yield req
		yield env.timeout(SAFE_TIME)


class Aircraft:
	'''
	构造飞机实例，飞机着陆的那一刻起，使用最短路径算法计算出飞机的默认路径，

	然后遍历所有处于滑行状态下的飞机，计算出可能冲突的节点，增加节点对应路段

	的权重，再重新计算出新的路径，直至新的路径没有重复节点或计算次数达到上限

	为止
	'''

	def __init__(self, env, res, attr):
		for k, v in attr.items():
			setattr(self, k, v)
		self.env = env
		self.res = res
		self.status = 'land'
		self.speed = AIRCRAFT_SPEED_TAXI
		self.action = env.process(self.run())
		self.keys = list(attr.keys())
		self.path = self.slide_path + self.departure_path
		self.plan_time = self._run_time()
		self.real_time = []
		self.conflict_time = 0


	# 着落时的路径列表
	@property
	def slide_path(self):
		return path[(self.landing_point, self.parking_point)]


	# 起飞时的路径列表
	@property
	def departure_path(self):
		return path[(self.parking_point, self.departure_point1)]



	# 计算计划的运行时间刘表
	def _run_time(self):
		plan_time = []
		edges = zip(self.path, self.path[1:])
		plan_time.append(self.landing_time)
		for edge in edges:
			start, end = edge
			if start == end:
				plan_time.append(plan_time[-1] + 5400)
			else:
				length = taxi_graph_1.edges[edge]['length']
				time = length / self.speed
				plan_time.append(plan_time[-1] + time)
		return plan_time


	# 计算发生冲突的节点
	@property
	def conflict_node(self):
		node = None
		for i, v in enumerate(self.plan_time):
			if self.real_time[i] - v >= 1:
				node = self.path[i]
		return node


	# # 计算冲突导致等待时间
	@property
	def conflict_times(self):
		return self.real_time[-1] - self.plan_time[-1]


	# 飞机着陆的那一刻，必须的初始化
	def init_path(self):
		pass


	def print_result(self):
		pass


	# def run(self):
	# 	yield self.env.timeout(self.landing_time - GLOBAL_TIMER)

	# 	self.init_path()


	# 	# self.opt_path(self.land_path, 1)
	# 	self.status = 'slide'
	# 	# print("%s land %s at %s" %(self.aircraft_id, self.path[0], self.env.now - 46200))
	# 	edges = zip(self.path, self.path[1:])
	# 	self.real_time.append(self.env.now - 46200)
	# 	for edge in edges:
	# 		start, end = edge
	# 		if start == end:
	# 			self.status = 'park'
	# 			yield self.env.timeout(5400)
	# 			self.real_time.append(self.env.now - 46200)
	# 			self.status = 'departure'
	# 			# print("%s departure %s at %s" % (self.aircraft_id, self.path[0], self.env.now - 46200))
	# 		else:
	# 			with self.res[end].request() as req:
	# 				stop_time = self.env.now
	# 				yield req
	# 				start_time = self.env.now
	# 				length = taxi_graph_1.edges[edge]['length']
	# 				time = length / self.speed
	# 				# 获取节点资源所等待的时间
	# 				waited = start_time - stop_time
	# 				# 如果路段长度小于安全间距，则等待
	# 				if SAFE_TIME > time:
	# 					yield self.env.timeout(time)
	# 				# 如果路段长度大于安全间距，则计算超出安全间距的部分的运行时间，如果运行时间大于等待时间
	# 				# 则通过此段路段的时间为飞机的直接通行的时间，如果小于等待时间，则该路段额通过时间为等待
	# 				# 时间加上安全间距部分的通行时间
	# 				else:
	# 					run = time - SAFE_TIME
	# 					if waited > run:
	# 						yield self.env.timeout(SAFE_TIME)
	# 					else:
	# 						yield self.env.timeout(time - waited)
	# 				self.real_time.append(self.env.now - 46200)
	# 				# prin


	def run(self):
		yield self.env.timeout(self.landing_time - GLOBAL_TIMER)
		self.status = 'slide'
		edges = zip(self.path, self.path[1:])
		self.real_time.append(self.env.now - 46200)
		for edge in edges:
			start, end = edge
			if start == end:
				self.status = 'park'
				yield self.env.timeout(5400)
				self.real_time.append(self.env.now - 46200)
				self.status = 'departure'
			else:
				length = taxi_graph_1.edges[edge]['length']
				time = length / self.speed
				# time = time - 4
				print(time)
				yield self.env.timeout(time)
				stop = self.env.now
				with self.res[end].request() as req:
					yield req
					self.real_time.append(self.env.now - 46200)
					start = self.env.now
					yield self.env.timeout(SAFE_TIME)
					self.conflict_time += start - stop

	# def  run(self):
	# 	yield self.env.timeout(self.landing_time - GLOBAL_TIMER)
	# 	self.status = 'slide'
	# 	edges = zip(self.path, self.path[1:])
	# 	# self.real_time.append(self.env.now - 46200)
	# 	for edge in edges:
	# 		start, end = edge
	# 		if start == end:
	# 			self.status = 'park'
	# 			yield self.env.timeout(5400)
	# 			self.real_time.append(self.env.now - 46200)
	# 			self.status = 'departure'
	# 		else:
	# 			node_dict.setdefault(end, 0)
	# 			length = taxi_graph_1.edges[edge]['length']
	# 			time = length / self.speed
	# 			yield self.env.timeout(time)
	# 			x = self.env.now - node_dict[end]
	# 			if x < SAFE_TIME:
	# 				yield self.env.timeout(SAFE_TIME - x)
	# 				self.conflict_time += SAFE_TIME - x
	# 			node_dict[end] = self.env.now
