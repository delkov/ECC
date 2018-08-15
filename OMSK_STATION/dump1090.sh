#!/bin/bash

path="/home/delkov/Documents/air"
cd $path

# probably net-ro-size can be 500, other params is ok.
./dump1090 --net --net-sbs-port 1487 --fix --ppm 0 --oversample --phase-enhance --net-ro-size 50 --net-ro-interval 1 --net-buffer 2 --quiet
