# ------------------- Stage 1: Build Stage ------------------------------
FROM python:3.8 AS backend-builder

# Set the working directory to /app
WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

# Copy the contents of the backend directory into the container at /app
COPY . /app/

# Install dependencies specified in requirements.txt


# ------------------- Stage 2: Final Stage ------------------------------

# Use a slim Python 3.9 image as the final base image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

RUN apt-get update && apt-get install -y libmariadb3

# Copy the built dependencies from the backend-builder stage
COPY --from=backend-builder /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/

# Copy the application code from the backend-builder stage
COPY --from=backend-builder /app /app

# Expose port 5000 for the Flask application
EXPOSE 5000

# Define the default command to run the application
CMD ["python", "app.py"]