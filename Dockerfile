FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a non-root user
RUN useradd -m appuser

WORKDIR /app

COPY . /app

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the ownership and permissions of the working directory
RUN chown -R appuser:appuser /app
RUN chmod -R 755 /app

# Switch to the non-root user
USER appuser

# Expose the port on which the application will run
EXPOSE 5000

# Start the Gunicorn server
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000"]
