import pymssql

class MSSQL:
	def __init__(self, host, user, pwd, db):
		self.host = host
		self.user = user
		self.pwd = pwd
		self.db = db

	def getConnect(self):
		if not self.db:
			return None
		self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, charset="utf8")
		cur = self.conn.cursor()
		if not cur:
			None
		else:
			return cur

	def execQuery(self, sql):
		cur = self.getConnect()
		cur.execute(sql)
		resList = cur.fetchall()

		# 查询完毕后必须关闭连接
		self.conn.close()
		return resList

	def execNonQuery(self, sql):
		cur = self.getConnect()
		cur.execute(sql)
		self.conn.commit()
		self.conn.close()




