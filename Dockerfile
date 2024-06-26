# Use an official Python runtime as a parent image
FROM python:3.11.1

# Set the working directory in the container
WORKDIR /app2

# Copy the current directory contents into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run gunicorn when the container launches
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:80", "main:app", "--timeout", "200", "--worker-class", "sync"]

