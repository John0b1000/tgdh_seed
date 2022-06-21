# Code Directory
This folder contains the source code for the TGDH implementation.
## Usage: driver.py
```
python3 driver.py -s <initial size> -i <unique member ID>
```
## Example:
Generate a tree with 4 nodes, i.e., group of 4 members.
This node/host/computer will have unique member ID 3.
```
python3 driver.py -s 4 -i 3
```
*This program can also be run as a script.*
## Command Line Instructions:
Different events can be specified from the command line:
  + Join Event: "j" or "join"
  + Leave Event: "l" or "leave"
  + Find Member Event: "m" or "member" 
  + Find Node Event: "n" or "node" 
  + Print Tree: "p" or "print"
  + Print Node Attributes: "vp" or "verbose print"
  + Update Tree: "u" or "update"
  + Quit/Exit Program: "q" or "quit"
## Examples:
Generate a tree with 4 members (I am member 1):
```
python3 code/driver.py -s 4 -i 1
```
Allow a new member to join:
```
>> Enter Event Here: j
```
Member 4 wants to leave: 
```
>> Enter Event Here: l
>> Enter leaving member ID: 4
```
Member 2 wants to leave:
```
>> Enter Event Here: l
>> Enter leaving member ID: 2
```
Find Member 5:
```
>> Enter event here: f
>> Would you like to find a member or node? m
>> Enter the member ID: 5
```
Find node <1,1>:
```
>> Enter event here: f
>> Would you like to find a member or node? n
>> Enter node index (l,v): 1,1
```
Print the tree to the terminal:
```
>> Enter event here: p
```
Print the attributes of all nodes:
```
>> Enter event here: vp
```
Quit the program:
```
>> Enter event here: q
```
