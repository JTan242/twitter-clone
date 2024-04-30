#!/bin/sh

files=$(find data/*)



echo '================================================================================'
echo 'loading tweets'
echo '================================================================================'
time parallel python3 load_tweets.py --db=postgresql://postgres:pass@localhost:2424 --inputs={} ::: $files
