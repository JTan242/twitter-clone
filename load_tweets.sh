#!/bin/sh

echo '==============================================================================='
echo 'loading tweets'
echo '==============================================================================='
time python3 load_data.py --db=postgresql://postgres:pass@localhost:2424 
