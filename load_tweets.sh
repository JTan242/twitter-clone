echo '================================================================================'
echo 'load pg_load_tweets'
echo '================================================================================'
time parallel python3 load_tweets.py --db=postgresql://postgres:pass@localhost:12346 --inputs={} ::: $files
