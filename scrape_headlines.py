#!/usr/bin/env python
# coding: utf-8

# In[48]:


import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd  # Added for Excel export
from datetime import date  # Import date

# Configuration
URL = 'https://citinewsroom.com/'
SENDER_EMAIL = 'annerquayeyt@gmail.com'
SENDER_PASSWORD = 'kqxg ybmq vshn niuj'
RECIPIENT_EMAIL = 'annerquaye@gmail.com'

def get_headlines():
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(URL, headers=headers)
    print(f"HTTP Status Code: {response.status_code}")  # Debug response status

    if response.status_code != 200:
        print("Failed to retrieve the webpage.")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = []  # Ensure it's a list

    try:
        # Updated selector for headlines
        for item in soup.select('.jeg_post_title a'):
            headline = item.get_text(strip=True)
            link = item.get('href')
            print(f"Found headline: {headline}, Link: {link}")  # Debug each headline and link
            headlines.append({'Headline': headline, 'Link': link})
    except AttributeError as e:
        print(f"Error: {e}")
        print("Debug info:", type(headlines), headlines)

    return headlines

# Save headlines to Excel
def save_to_excel(headlines):
    df = pd.DataFrame(headlines)
    today = date.today().isoformat()
    file_path = f'citinews_headlines_{today}.xlsx'
    df.to_excel(file_path, index=False)
    print(f"Headlines saved to {file_path}")
    return file_path

# Send email with attachment
def send_email(subject, body, attachment_path=None):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Attach the Excel file
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
        print("Email sent successfully.")  # Debug email success
    except Exception as e:
        print(f"Failed to send email: {e}")  # Debug email error

# Main execution
if __name__ == '__main__':
    headlines = get_headlines()
    today = date.today().isoformat()
    if headlines:
        excel_file = save_to_excel(headlines)
        body = f'Find attached the news referring to {today}.'
        send_email(f'Daily Headlines from Citi Newsroom - {today}', body, attachment_path=excel_file)
    else:
        send_email(f'Citi Newsroom Scraper - {today}', f'No headlines found on {today}.')


# In[ ]:




