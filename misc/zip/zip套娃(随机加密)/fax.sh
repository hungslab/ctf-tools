#!/usr/bin/env bash

while [ -e *.zip ]; do
    files=*.zip;
    for file in $files;do
        echo -n "Crack ${file}........";
        output="$(fcrackzip -u -l 1-5 -c '1' *.zip |tr -d '\n')";
        password="${output/PASSWORD FOUND\!\!\!\!: pw == /}";
        if [ -z "${password}" ]; then
            echo "FAIL\!\!\!\!\!";
            break 2;
        fi;
    echo "FOUND PASSWORD : '${password}'";
    unzip -q -P "${password}" "$file";
    rm "${file}";
    done;
done;
