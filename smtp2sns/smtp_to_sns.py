import os
import re
import asyncio
from email import policy
from email.parser import BytesParser
import boto3
from aiosmtpd.controller import Controller

AWS_REGION = os.environ.get("AWS_REGION","us-east-1")
TOPIC_ARN = os.environ.get("TOPIC_ARN","arn:invalid")
PORT = int(os.environ.get("SMTP_PORT", "1025"))

# AWS SNS client
sns_client = boto3.client('sns', region_name=AWS_REGION)  # Change region as needed

class SNSHandler:
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        if not address.endswith('@sms.sms'):
            return '550 not relaying to that domain'
        envelope.rcpt_tos.append(address)
        return '250 OK'
    async def handle_DATA(self, server, session, envelope):   
        print('Message from %s' % envelope.mail_from)
        print('Message for %s' % envelope.rcpt_tos)
        print('Message data:\n')
        for ln in envelope.content.decode('utf8', errors='replace').splitlines():
            print(f'> {ln}'.strip())
        print()
        print('End of message')
        send_message=False
        # Extract the phone number from the recipient email (e.g., 1234567890@sms.sms)
        for recipient in envelope.rcpt_tos:
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
                    send_message = True
                except Exception as e:
                    print(f"Failed to send SMS: {e}")
            else:
                print(f"No phone number found in recipient: {recipient}")
            if send_message:
                return '250 OK'
            else:
                return '550 Requested action not taken: not a valid phone email like: 123456@sms.sms'



async def run_server():
    handler = SNSHandler()
    controller = Controller(handler, hostname='0.0.0.0', port=PORT)
    print(f"SMTP server started on port {PORT}...")
    controller.start()

    # Keep the server running
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Shutting down server...")
        controller.stop()

if __name__ == "__main__":
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("Server stopped by user.")
    
