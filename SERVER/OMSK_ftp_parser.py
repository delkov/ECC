#!/usr/bin/env python3

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import sys
import psycopg2
from ast import literal_eval as make_tuple
from datetime import datetime, timedelta
import shutil
import os
import glob
import time
# import gzip
import time


path="/home/sammy/ftp/ftp_store/OMSK"
os.chdir(path)

# minimum_time=timedelta(seconds=10) # time between noise and air in DB, so should be bigger than 10sec

def not_double(s):
    try: 
        float(s)
        return False
    except ValueError:
        return True

def single_parse(entry):
	# calculate strange case for GPS

	# print('________________________________',entry[0], entry[1])
	# print('ENTRY', entry)
	if not_double(entry[15].split(';')[0]): # check oonly first gps param
		entry[15]='{0,0}'
	else:
		entry[15]='{'+entry[15].replace(';',',')+'}'

	# if not_double(entry[23]):
	# 	entry[23].split(' ')[0]=0
	# else:
	# 	pass

	if not_double(entry[23]):
		entry[22]=0
		entry[23]=0
	else:
		entry[23]=entry[23].split(' ')[0]
	

	check_list=[3,4,5,6,7,9,10,11,12,13,14,16,17,18,19,20,21]
	for x in check_list:
		if not_double(entry[x]):
			entry[x]=0
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
		entry[23], # ups_time
		)

	return sql_query

def main():
	global connect, cursor
	
	try:



		noise_query=[]
		file_list=sorted(glob.glob('OMSK*.txt')) # by default sort by name;	key = lambda file: os.path.getctime(file)) # find all txt in the folders
		# try:
		we_have_data=False


		if len(file_list)>0:
			SQL = '''SELECT id FROM omsk.noise ORDER BY id DESC LIMIT 1;'''
			cursor.execute(SQL)
			answer=cursor.fetchall()
			# check, wheter the table is empty
			if answer:
				last_ID=answer[0][0]
			else:
				last_ID=0
			# print(last_ID)


		successful_number=0


		for file_temp in file_list:
			# print(file_temp)
			with open(file_temp, 'r', encoding='cp1251') as txt:
				entry = list()
				all_strings=txt.readlines()
				
			for string in all_strings:
				value=string.strip().split('=')[1]
				entry.append(value)

			if len(entry)==0:
				continue
			# print('ENTRY', entry)
			sql_query = single_parse(entry)
			
			# CHECK, THAT WE HAVE time in air > than this noise time (means potential aircraft already in DB)
			
			# SQL = '''
			# SELECT (time_track) FROM omsk.tracks ORDER BY time_track desc LIMIT 1;
			# '''

			# cursor.execute(SQL)
			# last_time_air= cursor.fetchall()
			# print(last_time_air1)
			# if len(last_time_air)>0: # the table can be empty..
				# last_time_air=last_time_air[0][0]

			# else:
				# print('shutil')
				# shutil.move(file_temp, path+"/no_aircraft/"+file_temp)
				# continue # go to next file
			# print('LAST AIR:', last_time_air)
			# print('CURRENT NOISE:', sql_query[0])

			# if last_time_air-sql_query[0]>minimum_time or sql_query[0]-last_time_air>time_to_wait_sbs:#minimum_time: # if noise_time is greater than noise datetime by 10 sec -> fine
				# print('AIR IS ALREADY IN DB')
				# SQL = '''
				# SELECT (track, distance_1, time_track) FROM eco.tracks WHERE time_track - (%s) <=  INTERVAL '10 seconds' and (%s)-time_track <=  INTERVAL '10 seconds' and distance_1 IS NOT NULL ORDER BY distance_1 asc LIMIT 1;
				# '''

				# dont forget make index on time_track by CREATE INDEX idx_time_track ON eco.tracks ( time_track ); check index,  via \d eco.tracks;
				# CREATE INDEX time_dist_track ON eco.tracks  (time_track, distance_1, track);

			# SQL='''
			# SELECT (track, distance_1, time_track)
			#   FROM omsk.tracks 
			#   WHERE time_track >= (%s)::timestamp - INTERVAL '10 seconds'
			#     and time_track <= (%s)::timestamp + INTERVAL '10 seconds'
			#     and distance_1 IS NOT NULL
			# ORDER BY distance_1 asc LIMIT 1;
			# '''
			# # print('SQL QUERY', sql_query)
			# data = (sql_query[0],sql_query[0])
			# cursor.execute(SQL, data)
			# answer= cursor.fetchall()
		
			# if len(answer)==0: ## 
			# 	shutil.move(file_temp, path+"/no_aircraft/"+file_temp)
			track_distance=( None,None,None)
			# else:
			# 	we_have_data=True
			# 	track_distance=make_tuple(answer[0][0])

			last_ID=last_ID+1
			
			SQL = '''
			INSERT INTO omsk.noise (
			time_noise, base_name, stat_1, stat_2, stat_3, leq, slow, spectrum, meteo_stat, temperature,
			humadity, presure, wind, dir, gps_coordinate, gps_stat, temperature_core, temperature_mb, temperature_hdd, free_hdd,
			ups_stat, ups_mode, ups_time,  track, distance, aircraft_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,  %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,   %s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING;
			INSERT INTO omsk.noise_to_air (id) VALUES (%s); 
			'''

			data = sql_query + track_distance+(last_ID,)
			noise_query.append(cursor.mogrify(SQL, data).decode('utf-8'))
			os.remove(file_temp)




		# do it after processing of the all txt list 
			# if we_have_data:
		full_noise_query=''.join([x for x in noise_query])
				
		if len(full_noise_query)>0:
			# print('QUERY!!!',full_noise_query)
			cursor.execute(full_noise_query)
			connect.commit()



	except psycopg2.ProgrammingError as e:
		connect.rollback()
		print('something wrong with file  at time' +str(e) + str(datetime.now().strftime('%Y-%m-%d-%H-%M-%S')))
		shutil.move(file_temp, path+"/wrong_files/")
	# except psycopg2.InterfaceError as e:
		# print('AZAZA')

	except Exception as e:
		print(str(e))
		try:
			connect = psycopg2.connect(database='eco_db', user='postgres', host='localhost', password='z5UHwrg8', port=5432)
			cursor = connect.cursor()
		except Exception as e:
			print(str(e))









try:
	connect = psycopg2.connect(database='eco_db', user='postgres', host='localhost', password='z5UHwrg8', port=5432)
	cursor = connect.cursor()
except Exception as err:
	print('SQL connect problem')


print('FTP_PARSE start working'+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))) #str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


class ExampleHandler(FileSystemEventHandler):
    def on_created(self, event): # when file is created
        main()

observer = Observer()
event_handler = ExampleHandler() # create event handler
# set observer to use created handler in directory
observer.schedule(event_handler, path=path)
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


# -- Moscow
# INSERT INTO eco.static_points (name, lon, lat, alt) VALUES('Moscow', 37.515777, 55.873282, 0);
# WITH geom_1 AS (
# 	SELECT ST_Transform(ST_SetSRID(ST_MakePoint(37.515777, 55.873282), 4326), 32637) -- for South Korea,  32637 for MOSCOW, 32652 for Korea
# 	), point_3d AS (
# 	SELECT  ST_MakePoint(ST_X(st_transform),ST_Y(st_transform), 0) FROM geom_1
# 	) 
# UPDATE eco.static_points SET geom = (SELECT st_makepoint FROM point_3d) WHERE name = 'Moscow'; -- outut from above

# -- OMSK
# INSERT INTO omsk.static_points (name, lon, lat, alt) VALUES('omsk_1', 73.428965, 54.988934, 50);
# WITH geom_1 AS (
#     SELECT ST_Transform(ST_SetSRID(ST_MakePoint(73.428965, 54.988934), 4326), 32643) -- for South Korea,  32637 for MOSCOW, 32652 for Korea, 32643 - for OMSK
#     ), point_3d AS (
#     SELECT  ST_MakePoint(ST_X(st_transform),ST_Y(st_transform), 50) FROM geom_1
#     ) 
# UPDATE omsk.static_points SET geom = (SELECT st_makepoint FROM point_3d) WHERE name = 'omsk_1'; -- outut from above


# -- Korea
# INSERT INTO eco.static_points (name, lon, lat, alt) VALUES('Korea', 126.978899, 37.293873, 0);
# WITH geom_1 AS (
#     SELECT ST_Transform(ST_SetSRID(ST_MakePoint(126.978899, 37.293873), 4326), 32652) -- for South Korea,  32637 for MOSCOW, 32652 for Korea
#     ), point_3d AS (
#     SELECT  ST_MakePoint(ST_X(st_transform),ST_Y(st_transform), 0) FROM geom_1
#     ) 
# UPDATE eco.static_points SET geom = (SELECT st_makepoint FROM point_3d) WHERE name = 'Korea'; -- outut from above

