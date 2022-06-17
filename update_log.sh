#!/usr/bin/env bash

# This script is used to update the log file.
# It also undertakes the task of generating frequency variable.

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


# generate the level variable

# OLD_IFS="$IFS"

# IFS="="
# kv=(`grep run_frequency_level .env`)
# IFS="'"
# kv=(${kv[1]})

# level=${kv[1]}

# IFS="$OLD_IFS"

# # cp .env to running_frequency, because the .env file is special.
# cp .env running_frequency

level=`cat .env | grep -E -o "run_frequency_level='[0-9]+'"`
level=${level: 21}
level=${level%*\'}

# generate the frequency variable
mult=1
for i in $(seq 1 $level); do
    mult=$(($mult * 2))
done;
frequency=$(($mult * 3))
echo "new_frequency=$frequency"
echo $frequency > running_frequency