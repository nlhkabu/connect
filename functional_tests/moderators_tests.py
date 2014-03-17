from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.contrib.auth.models import User

# test what happens from the users' points of view
# ================================================

# Janine is a connect moderator and has been asked by a friend for an
# invitation.

# When she logs into connect, she sees a 'moderators' link in the menu.
# She clicks on the link and is taken to a page with a form for inviting new users

# She also sees a list of the user's she has already invited to the system,
# but who have not activated their account.

# She enters the details of her friend who she wants to invite:
# Lily
# Black
# lily@gmail.com

# When she submits the form, Lily now appears in her 'pending users' list.
# Lily's listing also includes the date and time Janine invited her
# and the options to resend or revoke the invitation.

# Janine tries to invite someone without a first name
# Janine tries to invite someone without a last name
# Janine tries to invite someone without an email address
# Janine tries to invite someone with an email address that is already registered.

# Janine tries to reinvite someone
# Janine revokes an invitation without a comment
# Janine revokes an invation with a comment

# Janine views the moderation logs
