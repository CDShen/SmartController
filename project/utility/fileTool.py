import os

##非递归查找文件加下文件数量
def find_file_num(src):
	if os.path.isdir(src):
		return len(os.listdir(src))
