# Use official Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy files to the container
COPY requirements.txt requirements.txt
COPY app.py app.py
COPY model.pkl model.pkl

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the API port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
