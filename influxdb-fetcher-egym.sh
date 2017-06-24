#!/bin/bash
script_dir=`dirname $0`
cd $script_dir
source bin/activate
python influxdb-fetcher-egym.py
