#!/bin/zsh

# file: tree_demo.sh
#

# sources:
# https://blog.eduonix.com/shell-scripting/generating-random-numbers-in-linux-shell-scripting/
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
	DIFF=$((i-2+1))
	j=$(($(($RANDOM%$DIFF))+2))
	code/driver.py -s $i -i $j
	sleep 1.2
    done
done

#
# end file: tree_demo.sh
