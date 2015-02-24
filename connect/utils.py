import crypt, random, re, string, time

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def generate_salt(size=8, chars=string.ascii_letters + string.digits):
    """
    Generates a random salt.
    """
    return ''.join(random.choice(chars) for _ in range(size))


def hash_time(salt='O2xqbWD9'):
    """
    Return a unique 30 character string based on the
    current timestamp. The returned string will consist
    of alphanumeric characters (A-Z, a-z, 0-9) only.

    Optionally accepts an eight character alphanumeric string,
    which is used as a salt.
    """
    hashed = ''
    salt = '$1$' + salt

    for pos in [-22, -8]:
        hashed += (crypt.crypt(str(time.time()), salt)[pos:].replace('/', '0')
                                                            .replace('.', '0'))
    return hashed


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
        'link_color': 'e51e41', # TODO: dynamically retrieve color from CSS
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
                      recipient_list=[recipient.email,],
                      html_message=html_body)

    return email
