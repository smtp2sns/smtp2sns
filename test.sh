#!/bin/bash

{
  printf "EHLO example.com\r\n"
  printf "MAIL FROM:<sender@example.com>\r\n"
  printf "RCPT TO:<1234567890@sms.sms>\r\n"
  printf "DATA\r\n"
  printf "From: sender@example.com\r\n"
  printf "To: 1234567890@sms.sms\r\n"
  printf "Subject: Test Email\r\n"
  printf "\r\n"  # Empty line to separate headers from body
  printf "This is a test email sent using netcat.\r\n"
  printf ".\r\n"  # End of DATA section
  printf "QUIT\r\n∫s"
} | nc localhost 1025
