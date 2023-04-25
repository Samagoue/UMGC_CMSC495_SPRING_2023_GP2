# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the entire project directory into the container
COPY . /app

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the command to start the Flask app
CMD ["flask", "run", "--port", "80"]
