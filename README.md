# Citi News Scraper

A Python script that automatically scrapes headlines from Citi Newsroom, saves them to an Excel file, and emails the results to specified recipients.

## Features

- Scrapes headlines and links from Citi Newsroom
- Saves data to Excel files with daily timestamps
- Sends automated emails with Excel attachments
- Configurable through JSON file
- Error handling and logging

## Prerequisites

- Python 3.6+
- Required Python packages:
  - requests
  - beautifulsoup4
  - pandas
  - openpyxl

## Configuration

Create a `config.json` file in the script directory with the following structure:

```json
{
    "URL": "your-target-url",
    "SENDER_EMAIL": "your-gmail-address",
    "SENDER_PASSWORD": "your-app-specific-password",
    "RECIPIENT_EMAIL": "recipient-email-address"
}
```

Note: For Gmail, you'll need to use an App-Specific Password. Two-factor authentication must be enabled on your Google Account to generate this.

## Installation

1. Clone this repository or download the script
2. Install required packages:
   ```bash
   pip install requests beautifulsoup4 pandas openpyxl
   ```
3. Create and configure your `config.json` file
4. Run the script:
   ```bash
   python scraper.py
   ```

## How It Works

1. **Web Scraping**: The script uses BeautifulSoup to parse the Citi Newsroom website and extract headlines and their corresponding links.

2. **Data Storage**: Retrieved headlines are saved to an Excel file with the naming format: `citinews_headlines_YYYY-MM-DD.xlsx`

3. **Email Notification**: The script sends an email with the Excel file attached. If no headlines are found, it sends a notification email without an attachment.

## Functions

- `get_headlines()`: Scrapes headlines and links from the configured URL
- `save_to_excel(headlines)`: Saves the scraped data to an Excel file
- `send_email(subject, body, attachment_path)`: Sends email with optional attachment

## Error Handling

The script includes error handling for:
- Failed web requests
- Parsing errors
- Email sending failures
- File operations

## Output

- Excel file with two columns: "Headline" and "Link"
- Email notification with the Excel file attached
- Console logging of operation status and errors

## Security Notes

- Store your `config.json` securely and never commit it to version control
- Use environment variables for sensitive data in production
- Follow Google's security best practices for email authentication

## License

This project is open source and available under the MIT License.
