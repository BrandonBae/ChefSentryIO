#!/bin/bash

# Step 1: Prune all docker containers and images
echo "Pruning all Docker containers and images..."
#sudo docker system prune -a -f
sudo docker system prune -f #Dont want to prune all images just dangling images (So we can take advantage of build cache?)

# Killing all running containers
echo "Killing all running Docker containers..."
sudo docker kill $(sudo docker ps -q)

# Step 2: Build the docker image
echo "Building the Docker image..."
sudo docker build -t chef-sentry .

# Step 3: Run the docker container
echo "Running the Docker container..."
sudo docker run --privileged --device=/dev/ -d -p 80:8080 chef-sentry

# Step 4: Attach to the running container to view output
echo "Attaching to the Docker container..."
container_id=$(sudo docker ps -l -q)
sudo docker attach $container_id

# End of script
echo "Script execution completed."

