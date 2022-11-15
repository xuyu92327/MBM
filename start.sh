#!/bin/bash

FILE=/home/muon_test$2.dat
if [ -f $FILE ]; then
    rm -f $FILE
fi

cd /tmp
./comet_wsf_ctrl << EOF
conf
dac set 4 $1
dac set 5 $1
start
quit
EOF

./comet_wsf_datadump -hitFile /home/muon_test$2.dat -exitTime 0

