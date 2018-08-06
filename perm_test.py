#!/usr/bin/env python3


import os
import glob
import time

path="/home/ssh_sammy/sbs_store/cutted_files"
os.chdir(path)

txt_list=sorted(glob.glob('cutted_sbs*.gz'))#, key = lambda file: os.path.getctime(file)) # find all txt in the folders
# print(txt_list)
for txt_temp in txt_list:
	print(txt_temp)
	os.remove(txt_temp)
	print('succesefully removed')
	# time.sleep(0.1)