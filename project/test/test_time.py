import datetime

import datetime
import time

now = datetime.datetime.now()
time = datetime.datetime.combine(datetime.date.today(),datetime.time(23,23,23) )
strTime = time.strftime('%Y-%m-%d %H:%M:%S')
print (strTime)
