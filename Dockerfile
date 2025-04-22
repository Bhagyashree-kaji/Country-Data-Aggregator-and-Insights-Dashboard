FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Make sure gunicorn is in your requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Explicitly install gunicorn (even if it's in requirements.txt, just to be safe)
RUN pip install gunicorn

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose the port
EXPOSE 5000

# Use the full path to gunicorn
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:5000", "main:app"]