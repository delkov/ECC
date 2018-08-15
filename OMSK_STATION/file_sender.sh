#!/bin/bash

path="/home/delkov/Documents/air/sbs_store/cutted_files/"
destination_path=ssh_sammy@195.9.26.246:/home/ssh_sammy/sbs_store/OMSK/
# max_txt_amount=60 # max umber of txt, then compressed to gz.

# change dir
cd $path


inotifywait -m -e create  "${path}" | while read NEWFILE
do
	list_of_txt=$(find . -name "OMSK_SBS*.txt")
	# echo $list_of_txt
	num_of_txt=$(echo $list_of_txt | wc -w)
	if [ $num_of_txt -gt 0 ]; then

		# list_of_gz=$(find . -name "*.gz")
		# num_of_gz=$(echo $list_of_gz | wc -w)
		# if [ $num_of_gz -gt 0 ]; then
			find . -name "*.gz" > list_of_files
			# echo $list_of_gz > list_of_files
			rsync -az  --files-from=list_of_files .  --remove-source-files -e "ssh -p 1488"  $destination_path # ssh-copy-id was done before
		# fi



		for file in $list_of_txt;   do gzip "$file";	done
		
		# for i in $(find . -name "*.gz")
		# do
		# 		rsync -az --remove-source-files -e "ssh -p 1488" $i $destination_path # ssh-copy-id was done before
		# done;

		# for i in $(find . -name "*.gz")
		# do
	 #    # echo "Welcome $i times"
		# 	rsync -az --remove-source-files -e "ssh -p 1488" $i $destination_path # ssh-copy-id was done before
		# done



	fi

done




# # while true

# while NEW_FILE=$(inotifywait --format %f -e create $path);do
# 	# start=`date +%s.%N`

# 	list_of_txt=$(find * -name "cutt*.txt")
# 	# #echo $list_of_txt
# 	num_of_txt=$(echo $list_of_txt | wc -w)
# 	if [ $num_of_txt -gt 0 ]; then
# 	# 	# echo $num_of_txt
# 	# 	# compress if needed
# 	# 	# if [ $num_of_txt -ge $max_txt_amount ]; then
# 	# 		# today=`date +%Y-%m-%d_%H_%M_%S` 
# 	# 		# echo "we should to compress, $today"
# 	# 		# filename="$today.tar.gz"
# 	# 		# cat $list_of_txt > merged.txt
# 	# 		# echo $list_of_txt | xargs rm -rf
# 	# 		# tar -czf  $filename merged.txt
# 	# 		# gzip $filename merged.txt
# 	# 	# else	
# 	# 		# echo "no need to merge"
# 		for file in $list_of_txt;   do gzip "$file";	done
# 		# fi


# 		# try to send all, we have (txt/gz)
# 			echo "azaz"
# 		# rsync -az --remove-source-files -e ssh $(find * -name "*.gz") $destination_path # ssh-copy-id was done before
# 	fi

# 	# end=`date +%s.%N`


# 	# sleep 10 sec
# 	# sleep 10
# done

# end=`date +%s.%N`

# echo "$end - $start" | bc -l 
