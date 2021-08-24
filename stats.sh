# A bash script that takes a list of urls from a text file, makes a request to each url and returns the status code for each request.
# Created with Codex of OpenAI
# Use as: ./stats.sh <file.txt>

#!/bin/bash

# Set the urls file to variable
file=$1

# Read through the file line by line
while read line
do
  # Get the status code from the request
  status_code=$(curl -s -o /dev/null -w "%{http_code}" $line)
  # Print the status code and url to the screen
  echo $status_code $line
done < $file
