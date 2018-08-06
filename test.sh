#!/bin/bash

destination_path=ssh_sammy@195.9.26.246:/home/ssh_sammy/sbs_store/cutted_files

# for i in $(find . -name "*.sh")
# do
   # echo "Welcome $i times"
	# rsync -az --remove-source-files -e "ssh -p 1488" $i $destination_path # ssh-copy-id was done before
# done

find . -name "*.sh" > list_of_files
# rsync -avz --files-from=/tmp/my_image_list.txt / cdn.example.com:/images/
# rsync -avz --files-from=test.txt -e "ssh -p 1488"  $destination_path # ssh-copy-id was done before
rsync -avz --files-from=list_of_files . -e "ssh -p 1488"  $destination_path # ssh-copy-id was done before
