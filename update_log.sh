#!/usr/env bash

# This script is used to update the log file.

# update README.md
echo "# 最新运行情况" > README.md
cat info.bak.log >> README.md

if [ -a info.log ]; then
    cat info.log >> info.bak.log
fi

mv info.bak.log info.log
