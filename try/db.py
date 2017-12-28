from config import DATABASE

import pymysql


def query(sql):
	conn = pymysql.connect(**DATABASE)
	with conn as cursor:
		cursor.execute(sql)
		result = cursor.fetchall()
	conn.close()
	return result