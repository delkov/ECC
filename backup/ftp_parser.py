#!/usr/bin/env python3

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys
import psycopg2
from ast import literal_eval as make_tuple
from datetime import datetime
import shutil
import os
import glob
import time
import gzip
import time


path="/home/delkov/Documents/air/FTP/ftp_store"
os.chdir(path)
maximum_size=700 # in bytes

def not_double(s):
    try: 
        float(s)
        return False
    except ValueError:
        return True

def single_parse(entry):
	# calculate strange case for GPS
	if not_double(entry[15].split(';')[0]): # check oonly first gps param
		entry[15]='{NULL,NULL}'
	else:
		entry[15]='{'+entry[15].replace(';',',')+'}'

	if not_double(entry[23]):
		entry[23].split(' ')[0]=None
	else:
		pass

	check_list=[3,4,5,6,7,9,10,11,12,13,14,16,17,18,19,20,21]
	for x in check_list:
		if not_double(entry[x]):
			entry[x]=None
		else:		
			pass


	day,month,year=map(int,entry[0].split('/'))
	str_time=entry[1].split('.')[0] 
	hour, minute, second = map(int,str_time.split(":"))

	sql_query=(
		# udatetime.from_string(entry[0].replace('/','-')+'T'+entry[1]).replace(tzinfo=None), #date_time for noise	
		datetime(year,month,day,hour,minute,second),
		entry[2], #base_name
		entry[3], #stat_1
		entry[4], #stat_2
		entry[5], # stat_3
		entry[6], # leq
		entry[7], # slow
		'{'+entry[8].replace(';',',')[:-1]+'}', # spectrum
		entry[9], # meteo_stat
		entry[10], # temper
		entry[11], # humad
		entry[12], # presu
		entry[13], # wind
		entry[14], # dir
		entry[15], # gps_coord
		entry[16], # gps stat
		int(float(entry[17])), # temperature_core
		int(float(entry[18])), # temperature_bd
		int(float(entry[19])), # temperature_hdd
		int(float(entry[20])), # free_hdd
		entry[21], # ups_stat
		entry[22], # umps_mode
		entry[23].split(' ')[0], # ups_time
		)

	return sql_query


def main():
	noise_query=[]
	file_list=sorted(glob.glob('*.txt'))# by default sort by name;	key = lambda file: os.path.getctime(file)) # find all txt in the folders
	# try:
	for file_temp in file_list:
		we_have_data=False

		with open(file_temp, 'r', encoding='cp1251') as txt:
			entry = list()
			all_strings=txt.readlines()
			
		for string in all_strings:
			value=string.strip().split('=')[1]
			entry.append(value)

		sql_query = single_parse(entry)
		SQL = '''
		SELECT (track) FROM eco.tracks WHERE time_track - (%s) <  INTERVAL '10 seconds' and (%s)-time_track <  INTERVAL '10 seconds' LIMIT 1;
		'''
		data = (sql_query[0],sql_query[0])
		cursor.execute(SQL, data)
		answer= cursor.fetchall()

		if len(answer)==0: ## 
			print('No data from aircraft yet.. lets wait')
			shutil.move(file_temp, path+"/no_data_from_air/"+file_temp)

		else: # we received data, do we have close aircraft?
			we_have_data=True
			SQL = '''
			SELECT (track, distance_1, time_track) FROM eco.tracks WHERE time_track - (%s) <  INTERVAL '10 seconds' and (%s)-time_track <  INTERVAL '10 seconds' and distance_1 IS NOT NULL ORDER BY distance_1 asc LIMIT 1;
			'''
			data = (sql_query[0],sql_query[0])
			cursor.execute(SQL, data)
			answer= cursor.fetchall()
		
			if len(answer)==0: ## 
				shutil.move(file_temp, path+"/no_aircraft/"+file_temp)
				track_distance=(None,None,None)
			else:
				track_distance=make_tuple(answer[0][0])
				os.remove(file_temp)

			SQL = '''
			INSERT INTO eco.noise (
			time_noise, base_name, stat_1, stat_2, stat_3, leq, slow, spectrum, meteo_stat, temperature,
			humadity, presure, wind, dir, gps_coordinate, gps_stat, temperature_core, temperature_mb, temperature_hdd, free_hdd,
			ups_stat, ups_mode, ups_time, track, distance, aircraft_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,  %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,   %s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING;
			'''
			data = sql_query + track_distance
			noise_query.append(cursor.mogrify(SQL, data).decode('utf-8'))

	if we_have_data:
		full_noise_query=''.join([x for x in noise_query])
		cursor.execute(full_noise_query)
		connect.commit()


try:
	connect = psycopg2.connect(database='eco_db', user='postgres', host='localhost', password='z5UHwrg8', port=5432)
	cursor = connect.cursor()
except Exception as err:
	print('SQL  connect problem')

print('FTP_PARSE start working'+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))) #str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


class ExampleHandler(FileSystemEventHandler):
    def on_created(self, event): # when file is created
        main()

observer = Observer()
event_handler = ExampleHandler() # create event handler
# set observer to use created handler in directory
observer.schedule(event_handler, path='/home/delkov/Documents/air/FTP/ftp_store')
observer.start()

# sleep until keyboard interrupt, then stop + rejoin the observer
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()


## CLOSE BD AFTER EXIT
# cursor.close()
# connect.close()