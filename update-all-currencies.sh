#!/bin/bash

rcp laptop:/home/erick/python/ta/*-prices.csv /home/erick/python/ta
rcp laptop:/home/erick/python/ta/cg-prices.log /home/erick/python/ta/

/home/erick/python/ta/cg-to-ohcl.py BTC
/home/erick/python/ta/cg-to-ohcl.py DOGE
/home/erick/python/ta/cg-to-ohcl.py ETH
/home/erick/python/ta/cg-to-ohcl.py FET
/home/erick/python/ta/cg-to-ohcl.py ICP
/home/erick/python/ta/cg-to-ohcl.py LTC
/home/erick/python/ta/cg-to-ohcl.py QNT
/home/erick/python/ta/cg-to-ohcl.py RNDR
/home/erick/python/ta/cg-to-ohcl.py SOL
/home/erick/python/ta/cg-to-ohcl.py GRT

