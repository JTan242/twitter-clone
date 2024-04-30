#!/bin/bash

failed=false

mkdir -p results

for problem in sql/*; do
    printf "$problem "
    problem_id=$(basename ${problem%.sql})
    result="results/$problem_id.out"
    expected="expected/$problem_id.out"
    psql < $problem > $result
    DIFF=$(diff -B $expected $result)
    if [ -z "$DIFF" ]; then
        echo pass
    else
        echo fail
        failed=true
    fi
done

if [ "$failed" = "true" ]; then
    exit 2
fi

