# Use the official image as a parent image FROM python:3.8
FROM python:3.9-slim


# Set the working directory in the container
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        netbase \
        && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY frontend.py frontend.py
COPY app.py app.py
COPY requirements.txt requirements.txt
COPY config.toml config.toml

RUN touch __init__.py

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define environment variable
ENV USDA_API_KEY=
ENV OPENAI_API_KEY=
ENV REPLICATE_API_KEY=



# Run app.py when the container launches
CMD ["streamlit", "run", "frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]
