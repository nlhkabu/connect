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
