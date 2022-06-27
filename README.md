# Tree-based Group Diffie-Hellman for SEED Emulator
This repo contains a Python implementation of TGDH encryption scheme for use on the [SEED Internet Emulator](https://github.com/seed-labs/seed-emulator). This implementation uses the Python library [anytree](https://anytree.readthedocs.io/en/latest/index.html). In order to generate tree visuals, [Graphviz](https://graphviz.org/) must be installed. 
## MacOS Installation
```
pip3 install anytree
```
```
brew install graphviz
```
## Ubuntu Installation
```
pip install anytree
```
```
sudo apt install graphviz
```
## Usage
***Important***: This demonstration is currently configured for use on the SEED Internet Emulator. Trying to run these programs locally or on multiple devices may cause issues to arise. Communication takes place using both multicast and end-to-end TCP connections.
### Initialization
To create a secure communication group, the following script must be run on the appropriate emulator nodes.
```
./run.sh -s <initial size> -i <unique member ID>
```
### Join Event
To add a new node to the group, run the following script. 
```
./join.sh
```
### Leave Event
To remove a node from the group, simply interrupt the `run.sh` or `join.sh` script.
```
Ctrl+C
```
## Example
The following series of commands is a simple demonstration using multiple nodes on the SEED emulator. The emulator script can be found above: 'subnet_demo.py'. The files `run.sh`, `join.sh`, and `multicast.config`, along with the `code` directory should be located in a shared folder: `tgdh`. This shared folder should be located in the same directory as the emulator script. 
### Step 0: Soldier 1 + Soldier 2 Create a Group
Soldier 1:
```
./run.sh -s 2 -i 1
```
Soldier 2:
```
./run.sh -s 2 -i 2
```
### Step 1: Soldier 3 Joins the Group
Soldier 3
```
./join.sh
```
### Step 2: Soldier 4 Joins the Group
Soldier 4:
```
./join.sh
```
### Step 3: Soldier 1 Leaves the Group
Soldier 1:
```
Ctrl+C
```
### Step 4: Soldier 4 Leaves the Group
Soldier 4:
```
Ctrl+C
```
### Step 5: Soldier 5 Joins the Group
Soldier 5:
```
./join.sh
```
### Step 6: Soldier 2 Leaves the Group
Soldier 2:
```
Ctrl+C
```
### Step 7: Soldier 5 Leaves the Group
Soldier 5:
```
Ctrl+C
```
The secure communication group is now closed.
