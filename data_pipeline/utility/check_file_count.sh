#!/bin/bash

# Set your starting directory
start_dir="."

# -type f is for files only, remove it if you want to count directories too
find "$start_dir" -type d | while read -r dir
do
  count=$(find "$dir" -type f | wc -l)
  echo "$dir has $count files"
done
