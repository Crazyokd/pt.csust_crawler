#!/usr/bin/env bash

# This script is used to dynamically adjust the frequency of program running.

# checkout master branch
git checkout master > /dev/null 2>&1

level=`dotenv get run_frequency_level`

# generate the frequency of program running
mult=1
for i in $(seq 1 $level); do
    mult=$(($mult * 2))
done;
frequency=$(($mult * 3))

# replace *\3 with *\${frequency}
sed -i 's/\*\/[0-9]\+/\*\/'"${frequency}"'/' .github/workflows/main.yml

# restore to instance branch 
git checkout instance > /dev/null 2>&1