# Use the official k6 image from Docker Hub
FROM grafana/k6:latest

# Set the working directory
WORKDIR /k6

# Copy your k6 scripts into the container
COPY . /k6/scripts


# Set the entrypoint to k6
ENTRYPOINT ["k6"]