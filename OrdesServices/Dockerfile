# OrdesServices/Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Copy the rest of the application code
COPY . /app

# Expose port 8000 (the port on which Django runs)
EXPOSE 8000

# Set Django settings module
# ENV DJANGO_SETTINGS_MODULE=OrdesServices.settings

# Run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
