# Use an official Python runtime as a parent image
FROM python:3.12.2

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file into the working directory
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app

# # Create a non-root user to run the application
# RUN useradd -m myuser
# USER myuser

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable if needed
ENV NAME World
ENV NAME World
ENV SERVICE_NAME CodeExecutionService


# Run app.py when the container launches
CMD ["python", "app.py"]
