#!/bin/bash

# Go to neo4j tabs
xte "keydown Alt_L" "key Tab" "keyup Alt_L"
sleep 0.05
xte "keydown Control_L" "key a" "keyup Control_L"
xte "keydown Control_L" "key v" "keyup Control_L"
xte "keydown Control_L" "key Return" "keyup Control_L"
# 'mouseclick 1'
while IFS='' read -r line || [[ -n "$line" ]]; do
    echo "$line" | xclip -selection clipboard
    sleep 0.1
    # Paste Text
    xte "keydown Control_L" "key v" "keyup Control_L"
    # execute command
    xte "sleep 0.1" "keydown Control_L" "key Return" "keyup Control_L"
    # wait 100 ms
    sleep 0.1
done < "$1"
