import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from django.conf import settings


def send(to_emails:list, subject:str, html_template:str, data:dict) -> bool:
    """
    to_emails: list of email addresses
    subject: email subject
    html: html template for the email
    data: information to replace in the template
    """
    f = open(settings.BASE_DIR / f'utilities/email_templates/{html_template}')
    template = f.read()
    for k,v in data.items():
        template = template.replace(k, v)
    f.close()
    message = Mail(
        from_email=os.environ.get('FROM_EMAIL'),
        to_emails=to_emails,
        subject=subject,
        html_content=template
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        return True
    except Exception as e:
        print(e)
        return False