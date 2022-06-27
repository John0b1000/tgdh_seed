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
**Important**: This demonstration is currently configured for use on the SEED Internet Emulator. Trying to run these programs locally or on multiple devices may cause issues to arise. 
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
Ctrl-C
```
