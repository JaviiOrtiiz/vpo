#!/bin/bash

# Navigate to the directory containing your repository
cd /home/pablo/vpo

# Pull the latest changes from the Git repository
git pull

# Stop and remove the old container if it exists
if [ "$(docker ps -q -f name=vpo)" ]; then
    docker stop vpo
    docker rm vpo
fi

# Remove the old Docker image if it exists
if [ "$(docker images -q vpo)" ]; then
    docker rmi vpo
fi

# Build the Docker image
docker build -t vpo .

# Run the run.sh script
sh run.sh
