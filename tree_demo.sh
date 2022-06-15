#!/bin/zsh

# file: tree_demo.sh
#

# this file loops and generates trees of various sizes
#

# run the TGDH program
#
x=1
while [ $x ]
do
    for i in {2..16}
    do
	./tgdh_v2.py -s $i -i 1
	sleep 1.2
    done
done

#
# end file: tree_demo.sh
