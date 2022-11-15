#!/bin/bash

FILE=/home/muon_test0.dat
if [ -f $FILE ]; then
    rm -f $FILE
fi

cd /tmp
./comet_wsf_ctrl << EOF
conf
dac set 2 2.33
dac set 3 2.33
dac set 4 2.43
dac set 5 2.43
asic set raw 1 0x7404
asic set raw 1 0x7c02
asic set raw 1 0xf004
asic set raw 1 0xfc04
asic set raw 0 0x4
asic set raw 0 0x406
asic set raw 0 0x804
asic set raw 0 0xc03
asic set raw 0 0x800a
asic set raw 0 0x8409
asic set raw 0 0x8808
asic set raw 0 0x8c07
start
quit
EOF

#./comet_wsf_datadump -rawPrint -hitFile /home/muon_test0.dat -exitTime 60
./comet_wsf_datadump -rawPrint -exitTime 0

./comet_wsf_ctrl << EOF
stop
quit
EOF
