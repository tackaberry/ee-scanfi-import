#!/bin/bash

source .env

# Name of your GCS bucket
bucket_name=$BUCKET  # Replace with your bucket name

# Directory containing the files to upload
source_directory="downloads"

# Check if the bucket exists
if ! gsutil ls "gs://$bucket_name"; then
  echo "Bucket gs://$bucket_name does not exist. Creating it..."
  gsutil mb "gs://$bucket_name"

  if [ $? -eq 0 ]; then
    echo "Bucket gs://$bucket_name created successfully."
  else
    echo "Error creating bucket gs://$bucket_name."
    exit 1
  fi
fi


# Upload files using gsutil -m for parallel upload
gsutil -m cp -r "$source_directory"/* "gs://$bucket_name/"

if [ $? -eq 0 ]; then
  echo "Files uploaded successfully to gs://$bucket_name"
else
  echo "Error uploading files to gs://$bucket_name"
  exit 1
fi