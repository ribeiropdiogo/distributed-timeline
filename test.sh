#!/bin/zsh

python3 benchmarking.py -p 9001 -tcp 9002 -u user1 -t 2 > test1.out &
python3 benchmarking.py -p 9003 -tcp 9004 -u user2 -t 3 > test2.out &
python3 benchmarking.py -p 9005 -tcp 9006 -u user3 -t 4 > test3.out &
python3 benchmarking.py -p 9007 -tcp 9008 -u user4 -t 5 > test4.out &
python3 benchmarking.py -p 9009 -tcp 9010 -u user5 -t 1 > test5.out &
