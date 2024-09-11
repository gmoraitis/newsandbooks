# Use the official Python image as a base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir flask requests flask_oidc PyJWT


#COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
# Expose the ports the app runs on
EXPOSE 5000
EXPOSE 5001

# Run the application
CMD ["sh", "-c", "python app.py & python ms.py"]

