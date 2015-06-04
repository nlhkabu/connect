import random
import re
import string
import time
import uuid

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def generate_unique_id():
    return str(uuid.uuid4()).replace('-', '')[:30]


def send_connect_email(subject, template, recipient, site, sender='',
                       url='', comments='', logged_against=''):
    """
    Sends an email to notify users and moderators of relevant events.
    Generates a plain text email from html template counterpart.
    """

    email_header_url = site.config.email_header.url
    email_header = ''.join(['http://', site.domain, email_header_url])

    template_vars = {
        'recipient': recipient,
        'site_name': site.name,
        'url': url,
        'sender': sender,
        'comments': comments,
        'logged_against': logged_against,
        'contact_email':  site.config.email,
        'email_header': email_header,
        # TODO: dynamically retrieve color from CSS
        'link_color': 'e51e41'
    }

    # Render HTML email:
    html_body = render_to_string(template, template_vars)

    # Render plain text email:
    text_body = html_body

    # Strip out HTML head section:
    p = re.compile('<head>(.|\s)*?</head>')
    text_body = p.sub('', text_body)
    # Strip out excessive whitespace:
    text_body = strip_tags(text_body).strip()
    p = re.compile('(\r|\n)(\x20|\t)+')
    text_body = p.sub('\n', text_body)
    p = re.compile('(\r|\n)(\r|\n)+')
    text_body = p.sub('\n\n', text_body)

    email = send_mail(subject=subject,
                      message=text_body,
                      from_email=site.config.email,
                      recipient_list=[recipient.email],
                      html_message=html_body)

    return email
