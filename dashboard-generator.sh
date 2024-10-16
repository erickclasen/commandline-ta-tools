#!/bin/bash
DIR="/home/erick/python/ta"
cd $DIR
echo "<html>"

echo "<body>"
echo "<head>"
echo "<TITLE>Satellite-A135 Server TA Dashboard</TITLE>"
echo "</head>"
echo "<H1>Satellite-A135 Server: TA Dashboard</H1>"
date
echo "<br>"

echo "<H2>Min 10 Day/Max 60 Day + Tenken & Kijun</H2>"
echo "<H3>BTC</H3>"
$DIR/rsi-fractals-avgs-bbands-txt-summary.py btc | grep Kijun
echo "<hr>"
echo "<H3>ETH</H3>"
$DIR/rsi-fractals-avgs-bbands-txt-summary.py eth | grep Kijun
echo "<hr>"
echo "<H3>ETH-BTC</H3>"
$DIR/rsi-fractals-avgs-bbands-txt-summary.py eth-btc | grep Kijun

echo "<hr>"
echo "<H2>Princeton-Newport: Most Up and Down Summary</H2>"

echo "<pre>"
$DIR/run-screener.sh | tail -n 12
echo "</pre>"


echo "<hr>"
echo "<H2>Coinmarket Cap Summary</H2>"

echo "<pre>"
cat $DIR/cg-prices.log
echo "</pre>"



echo "</body>"
echo "</html>"

