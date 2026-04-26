#!/bin/bash

if [[ ! -d "$1" ]]; then
    echo "Directory with voice pack incorrect: $1"
    exit 1
fi
curent=$(pwd)
timestamp=$(date +"%Y%m%d_%H%M%S")
file_name="pack_$timestamp.tar.gz"

cd "$1"
tar czf "$curent/$file_name" *
cd "$curent"
md5sum "$file_name"
