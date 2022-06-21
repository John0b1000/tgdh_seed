# Tree-based Group Diffie-Hellman for SEED Emulator
This repo contains a Python implementation of TGDH encryption scheme for use on the [SEED Internet Emulator](https://github.com/seed-labs/seed-emulator). This implementation uses the Python library [anytree](https://anytree.readthedocs.io/en/latest/index.html). In order to generate tree visuals, [Graphviz](https://graphviz.org/) must be installed (see below for macOS installation).
```
pip install anytree
```
```
brew install graphviz
```
## Usage: tree_demo.sh
*The function get_instructions must be commented out for this script to run (line 46 in driver.py).*

```
./tree_demo.sh
```
*Ensure execution permission is given:*

```
chmod a+x tree_demo.sh
```
