# Connect

Connect helps individuals connect with each other based on location, skills and interests.
Originally made for PyLadies - Connect was built so that users can connect based on skills, interests and location.

##  Demo

\# TODO: Add demo URL here

## Installation:

### Ubuntu:

```bash
sudo apt-get install libyaml-dev
sudo pip install virtualenv-wrapper
mkvirtualenv --python=/bin/python3 connect
pip install -r requirements/dev.txt
```

### Fedora:

```bash
sudo yum install libyaml-devel
sudo pip install virtualenv-wrapper
mkvirtualenv --python=/bin/python3 connect
pip install -r requirements/dev.txt
```

## Setting up connect for your group or organisation

### Site settings:

Configure the following in `connect/settings.py`:

- `SITE_ID`
- `SITE_URL`
- `SITE_EMAIL`
- `EMAIL_HOST`
- `EMAIL_PORT`
- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`
- `EMAIL_USE_TLS`

### Setting up the DB / Django Admin

```bash
python manage.py migrate
python manage.py loaddata accounts/fixtures/group_perms.yaml
```

#### Accounts: Brands

#### Accounts: Preferences

#### Auth: Groups

#### Auth: Permissions

#### Auth: Users

#### Sites: Site

#### Skills: Skills


### Customising colours

Connect is built with [Sass](http://sass-lang.com/). You can change the default pink highlight
color by editing the `$highlight` variable at the top of `_site_settings.scss`


## Misc.

### Font Awesome

Connect is currently integrated with [Font Awesome](https://fortawesome.github.io/Font-Awesome/) (v4.0.3)

### What's with functional tests?

As a newcomer to Django, I wanted to get into the habit of writing tests before code, but couldn't quite face the prospect of learning to code tests too.

So, I've written the tests as comments, so if I ever want/when I decide to come back and write them properly, I have a good outline to work from.
