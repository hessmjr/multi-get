# Use an official Python runtime as a parent image
FROM ubuntu:14.04
FROM python:2.7-slim

# Set the working directory to top level
WORKDIR multi-get/

# Copy the current directory contents into the container at
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install -e .

#CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"
ENTRYPOINT [ "python", "multiget" ]
