import os
import re
import asyncio
from email import message_from_bytes
from email.parser import BytesParser
import boto3
from aiosmtpd.controller import Controller
import logging

AWS_REGION = os.environ.get("AWS_REGION","us-east-1")
TOPIC_ARN = os.environ.get("TOPIC_ARN","arn:invalid")
PORT = int(os.environ.get("SMTP_PORT", "1025"))
MOCK_SERVICE = os.environ.get("MOCK_SERVICE")

# AWS SNS client
sns_client = boto3.client('sns', region_name=AWS_REGION)  # Change region as needed

# Create a logger for the SNSHandler class
logger = logging.getLogger("SNSHandler")

class SNSHandler:
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        logger.debug(f"Received RCPT command: {address}")
        if not address.endswith('@sms.sms'):
            logger.warning(f"Rejected recipient: {address} (invalid domain)")
            return '550 not relaying to that domain'
        envelope.rcpt_tos.append(address)
        logger.info(f"Accepted recipient: {address}")
        return '250 OK'
    async def handle_DATA(self, server, session, envelope):   
        logger.info(f"Received message from: {envelope.mail_from}")
        logger.info(f"Recipients: {envelope.rcpt_tos}")        
        body = ""
        email_message = message_from_bytes(envelope.content)
        if email_message.get_content_type() == "text/plain":
            body = email_message.get_payload(decode=True).decode('utf8', errors='replace')
        logger.debug(f"Message data: {body}")
        logger.debug("End of message")
        send_message=False
        send_message_id=""
        # Extract the phone number from the recipient email (e.g., 1234567890@sms.sms)
        for recipient in envelope.rcpt_tos:
            logger.debug(f"Processing recipient: {recipient}")
            match = re.match(r'(\d+)@', recipient)
            if match:
                phone_number = f"+{match.group(1)}"  # Add '+' for international format
                logger.info(f"Extracted phone number: {phone_number}")

                # Send SMS using Amazon SNS
                try:
                    logger.info("Attempting to send SMS...")                    
                    if not MOCK_SERVICE:
                        response = sns_client.publish(
                            PhoneNumber=phone_number,
                            Message=body,
                            TopicArn=TOPIC_ARN
                        )
                    else:
                        logger.info("MOCK_SERVICE: simulation")
                        response = {}
                        response['MessageId']="mock:1234"
                    logger.info(f"SMS sent to {phone_number}: Message ID: {response['MessageId']}")
                    send_message = True
                    send_message_id=response['MessageId']
                except Exception as e:
                    logger.error(f"failed to send SMS",e)
                    send_message_id=str(e)
            else:
                logger.error(f"No phone number found in recipient: {recipient}")
            if send_message:
                return f'250 OK: queued as {send_message_id}'
            else:
                return f'550 Requested action not taken: {send_message_id}'



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
    logging.basicConfig(
        level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
        handlers=[
            logging.StreamHandler(),  # Log to console
        ]
    )
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("Server stopped by user.")
    
