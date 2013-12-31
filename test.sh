#!/bin/sh
for i in 2 3 4 5 7 8 9
do 
    echo $i
    ./xml2json-badgerfish.py xj ${i}.xml > .test${i}.json || exit
    diff .test${i}.json ${i}.json || exit
    rm .test${i}.json
done

echo 'Success'