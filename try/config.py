import os

import pymysql


DATABASE = {
	# "host": "10.0.4.72",
	"host": "127.0.0.1",
	"user": "root",
	"password": "root",
	"db": "sf_e",
	"charset": "utf8",
	"cursorclass": pymysql.cursors.DictCursor
}

PROJECT_DIR = os.path.dirname(__file__)

# 飞机滑行速度
AIRCRAFT_SPEED_TAXI = 15 * 1.852 * 1000 * 1000 / 3600

# 机身长度
AIRCRAFT_LENGTH = 5000

# 飞机安全时间间隔
SAFE_TIME = 260 * 1000 / AIRCRAFT_SPEED_TAXI

# 仿真初始时间
GLOBAL_TIMER = -46200

# 飞机列队
AIR_LIST = []
