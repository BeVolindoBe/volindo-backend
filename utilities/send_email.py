import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from django.conf import settings


def send(to_emails:list, subject:str, html_template:str, data:dict) -> bool:
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
        sg.send(message)
        return True
    except Exception as e:
        return False
