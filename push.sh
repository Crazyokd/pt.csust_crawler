#!/usr/bin/env bash

# This script is used to push the code to the remote repository optionally.

# generate the pre_level variable
pre_frequency=`grep -E -o "\*/[0-9]+" .github/workflows/main.yml`
pre_frequency=${pre_frequency: 2}
echo "pre_frequency=$pre_frequency"

frequency=`cat running_frequency`
echo "new_frequency=$frequency"

if [ "$pre_frequency" = "$frequency" -o -z "$frequency" ]; then
    echo "The level is not changed, no need to push."
else
    sed -i 's/\*\/[0-9]\+/\*\/'"${frequency}"'/' .github/workflows/main.yml
    git add .
    git commit -m "chore: auto update the frequency of program running"    
fi