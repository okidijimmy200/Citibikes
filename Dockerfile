# Stage 1: Build the application
FROM prefecthq/prefect:2.7.7-python3.9 AS builder

# Set the working directory
WORKDIR /opt/prefect

# Copy the application code into the container
COPY . /opt/prefect

# Install dependencies
RUN pip install -r docker-requirements.txt --trusted-host pypi.python.org --no-cache-dir

# Stage 2: Create the final image with only necessary files
FROM prefecthq/prefect:2.7.7-python3.9

# Set the working directory
WORKDIR /opt/prefect

# Copy the application code and installed dependencies from the builder stage
COPY --from=builder /opt/prefect /opt/prefect





