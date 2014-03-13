from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.contrib.auth.models import User

# test what happens from the users' points of view
# ================================================

# Janine is a connect moderator and has been asked by a friend for an
# invitation.
