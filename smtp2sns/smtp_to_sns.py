import smtpd
import asyncore
import re
import boto3
from email.parser import BytesParser
from email.policy import default
import os

AWS_REGION = os.environ.get("AWS_REGION","us-east-1")
TOPIC_ARN = os.environ.get("TOPIC_ARN")

# AWS SNS client
sns_client = boto3.client('sns', region_name=AWS_REGION)  # Change region as needed

class SMTPHandler(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        print(f"Received message from: {mailfrom}")
        print(f"Recipients: {rcpttos}")
        print(f"Message data: {data.decode('utf-8')}")

        # Parse the email
        msg = BytesParser(policy=default).parsebytes(data)

        # Extract the phone number from the recipient email (e.g., 1234567890@sms.sms)
        for recipient in rcpttos:
            match = re.match(r'(\d+)@', recipient)
            if match:
                phone_number = f"+{match.group(1)}"  # Add '+' for international format
                print(f"Extracted phone number: {phone_number}")

                # Send SMS using Amazon SNS
                try:
                    response = sns_client.publish(
                        PhoneNumber=phone_number,
                        Message=msg.get_body(preferencelist=('plain')).get_content(),
                        TopicArn=TOPIC_ARN
                    )
                    print(f"SMS sent to {phone_number}: Message ID: {response['MessageId']}")
                except Exception as e:
                    print(f"Failed to send SMS: {e}")
            else:
                print(f"No phone number found in recipient: {recipient}")

if __name__ == "__main__":
    # Start SMTP server
    smtp_server = SMTPHandler(('0.0.0.0', 25), None)
    print("SMTP server started on port 25...")
    asyncore.loop()