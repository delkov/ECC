#!/usr/bin/env python3

from ast import literal_eval as make_tuple
import psycopg2
from datetime import datetime, timedelta
import os
import time

minimum_time=timedelta(seconds=10) # time between noise and air in DB, so should be bigger than 10sec

def main():
	global connect, cursor

	id_query=[]

	SQL = '''SELECT * FROM omsk.noise_to_air ORDER BY id ASC;'''
	cursor.execute(SQL)
	last_ID_list=cursor.fetchall()

	SQL = '''SELECT (time_track) FROM omsk.tracks ORDER BY time_track desc LIMIT 1;'''
	cursor.execute(SQL)
	last_time_air= cursor.fetchall()

	# print('LAST TIME TRACK', last_time_air)

	if len(last_time_air)>0: # the table can be empty..
		last_time_air=last_time_air[0][0]

		we_have_data=False
		for ID in last_ID_list:

			## separate query to not have a headache with formatiing.. since string+datetime..
			SQL='''SELECT (base_name) FROM omsk.noise WHERE id = (%s)'''
			data = ID
			cursor.execute(SQL, data)
			base_name = cursor.fetchall()[0][0]

			SQL='''SELECT (time_noise) FROM omsk.noise WHERE id = (%s)'''
			data = ID
			cursor.execute(SQL, data)
			time_noise = cursor.fetchall()[0][0]
			
			# print('BASE NAME', base_name)
			# print('TIME NOISE', time_noise)

			if last_time_air-time_noise>=minimum_time:#minimum_time: # if noise_time is greater than noise datetime by 10 sec -> fine
				# if base_name == VNK001 -> use distance_1, VNK002 -> distance_2
				# print('10 SEC PASSED!')

				SQL={
					'OMSK001': '''SELECT (track, distance_1, time_track)  FROM omsk.tracks  WHERE time_track >= (%s)::timestamp - INTERVAL '10 seconds'    and time_track <= (%s)::timestamp + INTERVAL '10 seconds' and distance_1 IS NOT NULL ORDER BY distance_1 asc LIMIT 1;''',
					'OMSK002': '''SELECT (track, distance_2, time_track)  FROM omsk.tracks  WHERE time_track >= (%s)::timestamp - INTERVAL '10 seconds'    and time_track <= (%s)::timestamp + INTERVAL '10 seconds' and distance_2 IS NOT NULL ORDER BY distance_2 asc LIMIT 1;''',
					'OMSK003': '''SELECT (track, distance_3, time_track)  FROM omsk.tracks  WHERE time_track >= (%s)::timestamp - INTERVAL '10 seconds'    and time_track <= (%s)::timestamp + INTERVAL '10 seconds' and distance_3 IS NOT NULL ORDER BY distance_3 asc LIMIT 1;''',
					'OMSK004': '''SELECT (track, distance_4, time_track)  FROM omsk.tracks  WHERE time_track >= (%s)::timestamp - INTERVAL '10 seconds'    and time_track <= (%s)::timestamp + INTERVAL '10 seconds' and distance_4 IS NOT NULL ORDER BY distance_4 asc LIMIT 1;'''						
				}

				SQL=SQL[base_name]
				data = (time_noise, time_noise)
				cursor.execute(SQL, data)
				track_distance= cursor.fetchall()

				# print('TRACK DISTANCE', track_distance)

				we_have_data=True
				if len(track_distance)==0: ##  no aircraft within 10 sec..
					SQL='''
						DELETE FROM omsk.noise_to_air WHERE id = (%s);
					'''
					data=ID
					# print('NO aircraft within 10s')
				else:
					SQL='''
						UPDATE omsk.noise SET (track, distance, aircraft_time) = (%s, %s, %s) WHERE id=(%s);
						DELETE FROM omsk.noise_to_air WHERE id = (%s);
					'''
					data=make_tuple(track_distance[0][0])+ID+ID
					# print('update noise ID: ', ID)

				id_query.append(cursor.mogrify(SQL, data).decode('utf-8'))

		if we_have_data:
			full_query_from_ID_list=''.join([x for x in id_query])
			cursor.execute(full_query_from_ID_list)
			connect.commit()



	# 	# CHECK, THAT WE HAVE time in air > than this noise time (means potential aircraft already in DB)
		
	# 	SQL = '''
	# 	SELECT (time_track) FROM eco.tracks ORDER BY time_track desc LIMIT 1;
	# 	'''

	# 	cursor.execute(SQL)
	# 	last_time_air= cursor.fetchall()
	# 	# print(last_time_air1)
	# 	if len(last_time_air)>0: # the table can be empty..
	# 		last_time_air=last_time_air[0][0]

	# 	else:
	# 		shutil.move(file_temp, path+"/no_aircraft/"+file_temp)
	# 		continue # go to next file
	# 	# print('LAST AIR:', last_time_air)
	# 	# print('CURRENT NOISE:', sql_query[0])

	# 	if last_time_air-sql_query[0]>minimum_time:#minimum_time: # if noise_time is greater than noise datetime by 10 sec -> fine

	# 		# dont forget make index on time_track by CREATE INDEX idx_time_track ON eco.tracks ( time_track ); check index,  via \d eco.tracks;
	# 		# CREATE INDEX time_dist_track ON eco.tracks  (time_track, distance_1, track);

	# 		SQL='''
	# 		SELECT (track, distance_1, time_track)
	# 		  FROM eco.tracks 
	# 		  WHERE time_track >= (%s)::timestamp - INTERVAL '10 seconds'
	# 		    and time_track <= (%s)::timestamp + INTERVAL '10 seconds'
	# 		    and distance_1 IS NOT NULL
	# 		ORDER BY distance_1 asc LIMIT 1;
	# 		'''
	# 		# print('SQL QUERY', sql_query)
	# 		data = (sql_query[0],sql_query[0])
	# 		cursor.execute(SQL, data)
	# 		answer= cursor.fetchall()
		
	# 		if len(answer)==0: ## 
	# 			shutil.move(file_temp, path+"/no_aircraft/"+file_temp)
	# 			track_distance=(None,None,None)
	# 		else:
	# 			we_have_data=True
	# 			track_distance=make_tuple(answer[0][0])
	# 			os.remove(file_temp)


	# 		SQL = '''
	# 		INSERT INTO eco.noise (
	# 		time_noise, base_name, stat_1, stat_2, stat_3, leq, slow, spectrum, meteo_stat, temperature,
	# 		humadity, presure, wind, dir, gps_coordinate, gps_stat, temperature_core, temperature_mb, temperature_hdd, free_hdd,
	# 		ups_stat, ups_mode, ups_time, track, distance, aircraft_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,  %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,   %s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING;
	# 		'''
	# 		data = sql_query + track_distance
	# 		noise_query.append(cursor.mogrify(SQL, data).decode('utf-8'))




	# # do it after processing of the all txt list 
	# if we_have_data:
	# 	full_noise_query=''.join([x for x in noise_query])
		
	# 	# print(full_noise_query)
	# 	cursor.execute(full_noise_query)
	# 	connect.commit()



	# except psycopg2.ProgrammingError as e:
	# 	connect.rollback()
	# 	print('something wrong with file  at time' +str(e) + str(datetime.now().strftime('%Y-%m-%d-%H-%M-%S')))
	# 	shutil.move(txt_temp, path+"/wrong_files/")
	# # except psycopg2.InterfaceError as e:
	# 	# print('AZAZA')

	# except Exception as e:
	# 	print(str(e))
	# 	try:
	# 		connect = psycopg2.connect(database='eco_db', user='postgres', host='localhost', password='z5UHwrg8', port=5432)
	# 		cursor = connect.cursor()
	# 	except Exception as e:
	# 		print(str(e))









try:
	connect = psycopg2.connect(database='eco_db', user='postgres', host='localhost', password='z5UHwrg8', port=5432)
	cursor = connect.cursor()
except Exception as err:
	print('SQL connect problem')



while True:
	time.sleep(10)
	main()

# print('FTP_PARSE start working'+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))) #str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


# class ExampleHandler(FileSystemEventHandler):
#     def on_created(self, event): # when file is created
#         main()

# observer = Observer()
# event_handler = ExampleHandler() # create event handler
# # set observer to use created handler in directory
# observer.schedule(event_handler, path=path)
# observer.start()

# # sleep until keyboard interrupt, then stop + rejoin the observer
# try:
#     while True:
#         time.sleep(1)
# except KeyboardInterrupt:
#     observer.stop()

# observer.join()


