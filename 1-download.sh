#!/bin/bash

# Set the directory where the text files are located
txt_dir="tif_files"

# Set the directory where downloaded files should be moved
download_dir="downloads"

# Create the download directory if it doesn't exist
mkdir -p "$download_dir"

# Loop through all text files in the directory
find "$txt_dir" -name "*.txt" -print0 | while IFS= read -r -d $'\0' txt_file; do
  # Read the URL from the text file
  url=$(cat "$txt_file")

  # Extract the filename from the URL (using basename and removing query parameters)
  filename=$(basename "$url" | cut -d'?' -f1)

  # Download the file using wget
  # -O specifies the output file
  # --content-disposition tries to use the server-suggested filename (if available)
  # -c allows resuming interrupted downloads
  # -t 3 sets the number of retries to 3
  # -T 10 sets the timeout to 10 seconds
  wget -O "$filename" --content-disposition -c -t 3 -T 10 "$url"

  # Check if the download was successful
  if [ $? -eq 0 ]; then
    # Move the downloaded file to the download directory
    mv "$filename" "$download_dir/$filename"
    echo "Downloaded and moved: $filename to $download_dir"
  else
    echo "Error downloading: $url"
  fi
done

echo "Finished processing files."