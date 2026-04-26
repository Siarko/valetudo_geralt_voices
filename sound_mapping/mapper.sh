#!/bin/bash

cleanup() {
    stty echo
}
trap cleanup EXIT

files_dir="$1"
if [ ! -d "$files_dir" ]; then
    echo "Incorrect sound directory given: "$files_dir
    exit
fi

start_number=0
if [ "$2" != "" ]; then
    start_number=$2
fi

echo "Starting from number "$start_number

if [ $start_number -gt 0 ]; then
    files=($(ls $files_dir | grep '.ogg' | sort -n | awk -F'.' '$1 >= '$start_number))
else
    files=($(ls $files_dir | grep '.ogg' | sort -n))
fi

if [ ${#files[@]} -eq 0 ]; then
    echo "No files found"
    exit 
else
    echo "Found "${#files[@]}" files, starting loop"
fi



cursor=0

function play() {
    mplayer $files_dir/$1
}

function render() {
    printf '\r\033[K'
    echo -n "> $1"
    
    local len=${#1}
    local back=$((len - cursor))
    if [ $back -gt 0 ]; then
        printf "\033[${back}D"
    fi
}
index=0
file="${files[$index]}"
chars=""
echo -n "> "

stty -echo

output="output.csv"
if [ "$start_number" == "0" ]; then
    echo "file,text_en" > $output
fi

previous_text=""
current_text=""


while [ 1 ]; do
    IFS= read -r  -n1 c
    if [[ "$c" == $'\e' ]]; then
        IFS= read -r -t 0.01 -n 10 rest
        c="$c$rest"
    fi

    if [[ "$c" == $'\e[A' ]]; then
        chars="$previous_text"
        cursor=${#chars}
        render "$chars"
    elif [[ "$c" == $'\e[B' ]]; then
        chars="$current_text"
        cursor=${#chars}
        render "$chars"
    elif [[ "$c" == $'\e[C' ]]; then
        if [ $cursor -lt ${#chars} ]; then
            cursor=$((cursor + 1))
        fi
        render "$chars"
    elif [[ "$c" == $'\e[D' ]]; then
        if [ $cursor -gt 0 ]; then
            cursor=$((cursor - 1))
        fi
        render "$chars"
    elif [[ "$c" == $'\e' ]]; then
        echo -e "\n ## REPLAY $file"
        play $file
        echo -e "\n"
        render "$chars"
    elif [[ "$c" == $'\177' || "$c" == $'\b' ]]; then
        if [ $cursor -gt 0 ]; then
            if [ $cursor -ne ${#chars} ]; then
                chars="${chars:0:$((cursor-1))}${chars:$cursor}"
            else
                chars="${chars%?}"
            fi
            cursor=$((cursor - 1))
        fi
        render "$chars"
    elif [[ "$c" == "" ]]; then
        if [[ "$chars" == "" ]]; then
            read -n1 -p "Empty input, you sure? " p
            if [[ "$p" != "y" ]]; then
                render $chars
                continue 
            fi
        else
            previous_text="$chars"
        fi

        echo "$file,\"$chars\"" >> $output

        chars=""
        current_text=""
        cursor=0
        index=$((index+1))
        file="${files[$index]}"
        if [ "$file" == "" ]; then
            echo "END"
            exit
        fi
        echo "\t Saved, Next file: $file"
        play $file
        render "$chars"
    else
        if [ $cursor -ne ${#chars} ]; then
            # Insert char at cursor
            chars="${chars:0:$cursor}$c${chars:$cursor}"
            cursor=$((cursor + 1))
        else
            chars=$chars$c
            cursor=${#chars}
        fi
        current_text="$chars"
        render "$chars"
    fi
done
