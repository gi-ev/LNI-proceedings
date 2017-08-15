#!/bin/bash
filename="$1"
tr -d '\r' < pages.txt | while read -r line
do
    echo "$line" | sed "sY^\([^ ]*\) \(.*\)Ysed -i \"sXstartpage{.*}Xstartpage{\2}X\" \1/paper.texY"
done > updatepages.sh
