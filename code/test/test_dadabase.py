import pymssql

class MSSQL:
	def __init__(self, host, user, pwd, db):
		self.host = host
		self.user = user
		self.pwd = pwd
		self.db = db

	def __GetConnect(self):
		if not self.db:
			raise (NameError, "没有设置数据库信息")
		self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, charset="utf8")
		cur = self.conn.cursor()
		if not cur:
			raise (NameError, "连接数据库失败")
		else:
			return cur

	def ExecQuery(self, sql):
		cur = self.__GetConnect()
		cur.execute(sql)
		resList = cur.fetchall()

		# 查询完毕后必须关闭连接
		self.conn.close()
		return resList

	def ExecNonQuery(self, sql):
		cur = self.__GetConnect()
		cur.execute(sql)
		self.conn.commit()
		self.conn.close()


ms = MSSQL(host="10.9.8.153", user="sa", pwd="123456", db="ATCSIM_VIRTUAL")
reslist = ms.ExecQuery("select * from airport")
for i in reslist:
	print (i)










