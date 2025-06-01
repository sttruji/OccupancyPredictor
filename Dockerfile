FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy contents
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run app
CMD ["uvicorn", "occupancy_api:app", "--host", "0.0.0.0", "--port", "8080"]