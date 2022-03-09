import boto3, os, time
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def today_date():
    return datetime.now().strftime("%d-%m-%Y")

def send_email_with_attachment(recipient):
    date = today_date()
    msg = MIMEMultipart()
    msg["Subject"] = f"tipster1X2 Predictions for {date}"
    msg["From"] = "dataslid@gmail.com"
    msg["To"] = recipient

    AWS_REGION = "us-east-1"

    # Set message body
    body = MIMEText("The PDF file is atteached below", "plain")
    msg.attach(body)

    filename = f"{date}_prediction.pdf"

    with open(filename, "rb") as attachment:
        part = MIMEApplication(attachment.read())
        part.add_header("Content-Disposition",
                        "attachment",
                        filename=filename)
    msg.attach(part)

    # Convert message to string and send
    email_key = os.environ.get("aws_key")
    email_secret = os.environ.get("aws_secret")
    client = boto3.client('ses',region_name=AWS_REGION, aws_access_key_id=email_key, aws_secret_access_key=email_secret)

    response = client.send_raw_email(
        Source="dataslid@gmail.com",
        Destinations=[recipient],
        RawMessage={"Data": msg.as_string()}
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("Email sent!")
    else:
        print("The email was not sent.")
    
    time.sleep(10)