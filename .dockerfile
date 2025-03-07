# Use the official Python 3.10.8 image as the base image
FROM python:3.10.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . ./

# Command to run the application (modify as per your application entry point)
CMD ["streamlit","run","app.py"]