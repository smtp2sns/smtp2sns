# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the script and install dependencies
COPY smtp_to_sns.py .
RUN pip install boto3

# Expose SMTP port
EXPOSE 25

# Run the script
CMD ["python3", "smtp_to_sns.py"]