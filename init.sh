#!/bin/bash

cd /boot/efi
./loadfirmware.sh

cd /tmp
insmod ./alteldma.ko

