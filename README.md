# influxdb-fetcher-egym
Script to fetch e-gym (www.egym.de) data and put it into influxdb


This project is forked from the apparently dormant project bitstacker/influxdb-fetcher-egym

My version fetches as much metrix as possible, no longer based on session date, but on actual exercise dates and times.  This provides more accuracy and also makes other calculations possible
For this script to work, edit rename config.example.yml to config.yml and add your own data. You also need my fork of the python-egym api interface (https://github.com/marcelpoelstra/python-egym). 

Note:  Setting the (default) 7 days history to larger number of dates seems to become unrelyable at some point.)
So to be sure to get everything, make sure to run this script at least once every 5 days or so.

