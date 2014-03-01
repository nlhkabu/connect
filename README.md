# Connect

Connect helps individuals connect with each other based on location, skills and interests.
Originally made for PyLadies - connect was built so that users can connect based on Python skills, interests and location.

##  Demo

TODO: Demo URL here

## Setting up connect for your group or organisation

### settings.py

Configure the following:

-  SITE_ID
-  SITE_URL
-  EMAIL_HOST
-  EMAIL_PORT
-  EMAIL_HOST_USER
-  EMAIL_HOST_PASSWORD
-  EMAIL_USE_TLS

### Setting up the DB / Django Admin

#### Accounts: Brands

#### Accounts: Preferences

#### Auth: Groups

#### Auth: Permissions

#### Auth: Users

#### Sites: Site

#### Skills: Skills


### Customising colours

Connect is built with SCSS.  You can change the default pink highlight
color by editing the $highlight variable at the top of _site_settings.scss


## Misc.

### Font Awesome

Connect is currently integrated with Font Awesome v4.0.3

### What's with functional tests?

As a newcomer to Django, I wanted to get into the habit of writing tests before code, but couldn't quite face the prospect of learning to code tests too.

So, I've written the tests as comments, so if I ever want/when I decide to come back and write them properly, I have a good outline to work from.
