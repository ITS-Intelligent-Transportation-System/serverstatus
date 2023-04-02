#!/home/apps/python-venv/bin/python3

import logging
import psutil
import socket
import mysql.connector
from configobj import ConfigObj
from datetime import datetime

__version__ = "230327.1305"


# ============== STARTING PROGRAM HERE ==============
if __name__ == "__main__":
	config_file = "/etc/vcounting/serverstatus.cfg"
	conf = ConfigObj(config_file)

	format = "%(asctime)s: %(message)s"
	logging.basicConfig(format=format, level=logging.INFO, datefmt=conf['log']['timeformat'], filename=conf['log']['file'] )
	logging.info("[vCOUNTING] ============== STARTING PROGRAM ==============")
	logging.info("[vCOUNTING] reading configuration at %s", config_file)


	mysqlConfig = { 'user':conf['mysql']['username'], 'password':conf['mysql']['password'], 'host':conf['mysql']['host'], 'database':conf['mysql']['database'], 'raise_on_warnings': True}
	query = "INSERT INTO `server` (`id`,`hostname`,`timestamp`,`cpu_count`,`cpu_load`,`memory_percentage`,`disk1_mountpoint`,`disk1_usage`,`disk2_mountpoint`,`disk2_usage`,`disk3_mountpoint`,`disk3_usage`,`disk4_mountpoint`,`disk4_usage`,`disk5_mountpoint`,`disk5_usage`) VALUES (NULL,'{hostname}','{now}','{cpu_count}','{cpu_percent}','{memory_usage}','{disk1_mountpoint}','{disk1_usage}','{disk2_mountpoint}','{disk2_usage}','{disk3_mountpoint}','{disk3_usage}','{disk4_mountpoint}','{disk4_usage}','{disk5_mountpoint}','{disk5_usage}');"

	now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	hostname = socket.gethostname()
	cpu_count = psutil.cpu_count()
	cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
	memory_usage = psutil.virtual_memory().percent

	print(now)

#	for i in range(5):
#		if conf['mountpoint']['mp-{}'.format(i)] != '':
#			print(conf['mountpoint']['mp-{}'.format(i)], psutil.disk_usage(conf['mountpoint']['mp-{}'.format(i)]).percent)

	if (conf['mountpoint']['mp-0'] != ''):
		mp0_percent = psutil.disk_usage(conf['mountpoint']['mp-0']).percent
	else:
		mp0_percent = 0.00

	if (conf['mountpoint']['mp-1'] != ''):
		mp1_percent = psutil.disk_usage(conf['mountpoint']['mp-1']).percent
	else:
		mp1_percent = 0.00

	if (conf['mountpoint']['mp-2'] != ''):
		mp2_percent = psutil.disk_usage(conf['mountpoint']['mp-2']).percent
	else:
		mp2_percent = 0.00

	if (conf['mountpoint']['mp-3'] != ''):
		mp3_percent = psutil.disk_usage(conf['mountpoint']['mp-3']).percent
	else:
		mp3_percent = 0.00

	if (conf['mountpoint']['mp-4'] != ''):
		mp4_percent = psutil.disk_usage(conf['mountpoint']['mp-4']).percent
	else:
		mp4_percent = 0.00

	try:
		db = mysql.connector.connect(**mysqlConfig)
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			logging.info("[vCOUNTING][ERROR] Something is wrong with your MySQL username or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			logging.info("[vCOUNTING][ERROR] MySQL Database not exist")
		else:
			resultAPI = err
	else:
		cursor = db.cursor()
		cursor.execute(query.format(now=now,hostname=hostname,cpu_count=cpu_count,cpu_percent=cpu_percent,memory_usage=memory_usage,disk1_mountpoint=conf['mountpoint']['mp-0'],disk1_usage=mp0_percent,disk2_mountpoint=conf['mountpoint']['mp-1'],disk2_usage=mp1_percent,disk3_mountpoint=conf['mountpoint']['mp-2'],disk3_usage=mp2_percent,disk4_mountpoint=conf['mountpoint']['mp-3'],disk4_usage=mp3_percent,disk5_mountpoint=conf['mountpoint']['mp-4'],disk5_usage=mp4_percent))
		db.commit()
		db.close()

#	print(query.format(now=now,hostname=hostname,cpu_count=cpu_count,cpu_percent=cpu_percent,memory_usage=memory_usage,disk1_mountpoint=conf['mountpoint']['mp-0'],disk1_usage=mp0_percent,disk2_mountpoint=conf['mountpoint']['mp-1'],disk2_usage=mp1_percent,disk3_mountpoint=conf['mountpoint']['mp-2'],disk3_usage=mp2_percent,disk4_mountpoint=conf['mountpoint']['mp-3'],disk4_usage=mp3_percent,disk5_mountpoint=conf['mountpoint']['mp-4'],disk5_usage=mp4_percent))
#	print(now)
#	print(hostname)
#	print(cpu_count)
#	print(cpu_percent)
#	print(memory_usage)
#	print(conf['mountpoint']['mp-0'], mp0_percent)
#	print(conf['mountpoint']['mp-1'], mp1_percent)
#	print(conf['mountpoint']['mp-2'], mp2_percent)
#	print(conf['mountpoint']['mp-3'], mp3_percent)
#	print(conf['mountpoint']['mp-4'], mp4_percent)


#	print("=============== END-OF PROGRAM ===============")
