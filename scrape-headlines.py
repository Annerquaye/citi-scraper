#!/usr/bin/env python
# coding: utf-8

# In[56]:


import json
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
from datetime import date

# Load configuration
import os
URL = 'https://citinewsroom.com'
SOME_SECRET = os.getenv('SOME_SECRET')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL')


def get_headlines():
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(URL, headers=headers)
    print(f"HTTP Status Code: {response.status_code}")

    if response.status_code != 200:
        print("Failed to retrieve the webpage.")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = []

    try:
        for item in soup.select('.jeg_post_title a'):
            headline = item.get_text(strip=True)
            link = item.get('href')
            print(f"Found headline: {headline}, Link: {link}")
            headlines.append({'Headline': headline, 'Link': link})
    except AttributeError as e:
        print(f"Error: {e}")
        print("Debug info:", type(headlines), headlines)

    return headlines

def save_to_excel(headlines):
    df = pd.DataFrame(headlines)
    today = date.today().isoformat()
    file_path = f'citinews_headlines_{today}.xlsx'
    df.to_excel(file_path, index=False)
    print(f"Headlines saved to {file_path}")
    return file_path

def send_email(subject, body, attachment_path=None):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    if attachment_path:
        with open(attachment_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={attachment_path}')
        msg.attach(part)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == '__main__':
    headlines = get_headlines()
    today = date.today().isoformat()
    if headlines:
        excel_file = save_to_excel(headlines)
        body = f'Find attached the news referring to {today}.'
        send_email(f'Daily Headlines from Citi Newsroom - {today}', body, attachment_path=excel_file)
    else:
        send_email(f'Citi Newsroom Scraper - {today}', f'No headlines found on {today}.')

