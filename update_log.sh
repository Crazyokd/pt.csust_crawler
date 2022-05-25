#!/usr/env bash

# This script is used to update the log file.

# update README.md
echo "# 最新运行情况" > README.md
cat info.bak.log >> README.md

if [ -a info.log ]; then
    cat info.log >> info.bak.log
fi

mv info.bak.log info.log

# get the size of the log file
size=`wc -c info.log | cut -f 1 -d " "`
# limit the size of the log file to 196kb
if [ $size -ge 196000 ]; then
    # delete half of the content
    line=`wc -l info.log | cut -f 1 -d " "`
    line=$(($line / 2))

    for i in $(seq 1 $line); do
        sed -i '$d' info.log;
    done;
    echo "The log file is too large, delete half of the content."
fi