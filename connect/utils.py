import crypt, random, re, string, time

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
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


def generate_html_email(subject, from_address, recipients,
                        html_template, template_vars={}, txt_template=None):
    '''
    Generate and return a HTML email with plain text counterpart. Recipients
    should be passed in as a list.
    '''
    # Render HTML email:
    html_body = render_to_string(html_template, template_vars)

    # Render plain text email:
    if not txt_template and html_template[-5:] == '.html':
        txt_template = html_template.replace('.html', '.txt')

    try:
        text_body = render_to_string(txt_template, template_vars)
    except:
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

    # Create email, and attach HTML alternative version:
    email = EmailMultiAlternatives(
        subject,
        text_body,
        from_address,
        recipients,
    )
    email.attach_alternative(html_body, "text/html")

    return email


def send_connect_email(subject, template, recipient, site, sender='',
                       url='', comments='', logged_against=''):
    """
    Sends an email to notify users and moderators of relevant events.
    e.g. account activation, abuse decisions, new account applications, etc.
    """

    template_vars = {
        'recipient': recipient,
        'site_name': site.name,
        'url': url,
        'sender': sender,
        'comments': comments,
        'logged_against': logged_against,
        'contact_email':  site.email,
    }

    email = generate_html_email(
        subject,
        settings.EMAIL_HOST_USER,
        [recipient.email],
        template,
        template_vars,
    )

    email.send()
