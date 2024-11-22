#!/bin/bash 
DIR="/home/erick/python/ta"


rm $DIR/output-rsi-er-price-sma20-multiple.csv

$DIR/rsi-fractals-avgs-bbands-txt-summary.py BTC
$DIR/rsi-fractals-avgs-bbands-txt-summary.py DOGE
$DIR/rsi-fractals-avgs-bbands-txt-summary.py ETH
$DIR/rsi-fractals-avgs-bbands-txt-summary.py FET
$DIR/rsi-fractals-avgs-bbands-txt-summary.py GRT
$DIR/rsi-fractals-avgs-bbands-txt-summary.py ICP
$DIR/rsi-fractals-avgs-bbands-txt-summary.py LTC
$DIR/rsi-fractals-avgs-bbands-txt-summary.py QNT
$DIR/rsi-fractals-avgs-bbands-txt-summary.py RNDR
$DIR/rsi-fractals-avgs-bbands-txt-summary.py SOL

# Combos
$DIR/rsi-fractals-avgs-bbands-txt-summary.py INDEX
$DIR/rsi-fractals-avgs-bbands-txt-summary.py ETH-BTC



echo
echo "Cur  ,Und,Targt,RSI, ER,20Ml,Mayer,TFR,  Volat"


# Sort by desending price/sma20 multiples
sort -nk6 -t, -r $DIR/output-rsi-er-price-sma20-multiple.csv


