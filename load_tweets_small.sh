#!/bin/sh

echo '================================================================================'
echo 'loading tweets'
echo '================================================================================'
time python3 load_data_small.py --db=postgresql://postgres:pass@localhost:2424 
