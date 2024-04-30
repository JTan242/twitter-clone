echo '================================================================================'
echo 'load pg_load_tweets'
echo '================================================================================'
echo "$files" | time parallel python3 -u load_tweets_batch.py --db=postgresql://postgres:pass@localhost:2424 --inputs {}
