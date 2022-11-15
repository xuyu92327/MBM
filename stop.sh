#!/bin/bash

cd /tmp
./comet_wsf_ctrl << EOF
stop
quit
EOF

pkill -f data
