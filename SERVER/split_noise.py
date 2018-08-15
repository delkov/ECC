#!/usr/bin/env python3


from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import gzip
import os
import glob
import time


path="/home/sammy/ftp/ftp_store"
os.chdir(path)


def main():	
	file_list=sorted(glob.glob('*.gz')) # find all txt in the folders
	for file_temp in file_list:
		with gzip.open(file_temp,'rb') as gz:
			data=str(gz.read(),'cp1251').splitlines()
		
		# new=0
		counter=-1
		content_for_single_txt=[]

		for line in data:
			# if new==3:
				# brea2k
			# print(line)
			counter=counter+1
			if counter % 24==23:
				# new=new+1

				counter=-1
				filename=content_for_single_txt[0].split('=')[1].replace('/','_')+'_'+content_for_single_txt[1].split('=')[1].replace(':','_')+'.txt'
				# print('________NEW txt', filename)
				content_for_single_txt.append(line)


				what_to_write="\n".join(content_for_single_txt)+'\n'
				with open(filename, 'a') as out:
					out.write(what_to_write)

				
				content_for_single_txt=[]
			else:
				# print(line)
				content_for_single_txt.append(line)
			# print(line)
		
		# print('new txt')
		# print(content_for_single_txt[0].split('=')[1].replace('/','-')+' '+content_for_single_txt[1].split('=')[1])
		# with open(filename, 'a') as out:
			# what_to_write="\n".join(content_for_single_txt)+'\n'
			# out.write(what_to_write)
		os.remove(file_temp)

while True:
	main()
	time.sleep(10)