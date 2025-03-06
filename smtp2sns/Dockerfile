# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the script and install dependencies
RUN pip install boto3 aiosmtpd
COPY smtp_to_sns.py .
# Expose SMTP port
EXPOSE 1025

# Run the script
CMD ["python3", "smtp_to_sns.py"]
