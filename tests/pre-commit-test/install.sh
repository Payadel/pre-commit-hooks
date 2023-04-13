#!/bin/bash

dist_dir="../../dist"
poetry_dir="../../"

directories=("$dist_dir" "$poetry_dir")
for dir in "${directories[@]}"; do
  if [ ! -d "$dir" ]; then
    echo "Can not find dir: $dist_dir"
    exit 1
  fi
done

# Use find command to search for files with the .tar.gz extension and save result in variable
result=$(find "$dist_dir" -name "*.tar.gz")

# Count number of files found
count=$(echo "$result" | wc -l)

# If no file or more than one file is found, print error message and exit
if [ "$count" -eq 0 ]; then
  echo "Error: no .tar.gz file found in dist_dir '$dist_dir'"
  exit 1
elif [ "$count" -gt 1 ]; then
  echo "Error: multiple .tar.gz files found in dist_dir '$dist_dir'"
  exit 1
fi

(cd "$poetry_dir" && poetry build) && pip install --upgrade "$result"
