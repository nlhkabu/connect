from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.contrib.auth.models import User

# test what happens from the users' points of view
# ================================================

class MemberVisitTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_login_via_login_page(self):

        sam = User.objects.create_user(username="sam", email="sam@example.com", password="pass")

        # Sam visits the connect homepage and sees that she needs to login
        self.browser.get(self.live_server_url)
        self.assertIn('Login', self.browser.title)

        # There she sees a login form with username and password fields
        input_username = self.browser.find_element_by_id('id_username')
        input_password = self.browser.find_element_by_id('id_password')

        # Sam enters her username and an incorrect password
        input_username.send_keys('sam')
        input_password.send_keys('wrongpass')
        input_password.send_keys(Keys.ENTER)

        # But is told that the username and password do not match
        error_message = self.browser.find_element_by_id('login-error') #TODO: Add a cleaner error message

        # She tries again, this time with the correct password
        input_password = self.browser.find_element_by_id('id_password')

        input_password.send_keys('pass')
        input_password.send_keys(Keys.ENTER)

        # Success! She is redirected to the connect dashboard
        self.assertIn('Dashboard', self.browser.title)


# There she sees:

# A card for each member registered on the site, with:
# Member name
# Member photo
#   Uploaded img (if they have one)
#   OR gravatar (if they have one)
#   ELSE a default image
# Member connect preferences
# Member skills (and their proficiency)
# Member bio
# Member links

# Sam notices a form on the page where she can 'Refine' her search

# SKILLS/INTERESTS

# When she selects 'Django' and clicks on 'submit', she notices that
# the members she sees all have the skill 'Django'

# When she selects 'Django' and 'Game Development' she sees all of
# the members with the skills 'Django' OR 'Game Development'

# CONNECT PREFERENCES

# Sam also notices that she can filter results by their connect preferences.
# She selects 'Mentor' to see all of the members who have the preference 'mentor'.
# Likewise, when she selects 'Mentor' and 'Mentee' she sees all of the members
# with the preferences 'Mentor' OR 'Game Development'

# Sam notices that she can filter members by BOTH skill/interest & connect preference.
# She is looking for a Django mentor, so selects 'Django' and 'Mentor'
# All of the members listed in the results have the skill 'Django' and the
# preference 'Mentor'.

# Sam is also making a Python game and is looking for members to join her.
# She selects 'Game Development' and 'Coding Buddy', but there is nobody in
# the system who matches this search, so she sees a 'no results' message.

# MY ACCOUNT

# Sam notices a link at the top right called 'My Account'.
# When she clicks on the link, she is taken to a page where she sees her
# 'profile' settings.

# Here she sees:
# Her Name
# Her Biography
# Her gravatar image (if she has one)
#     OR if she has uploaded a different image, she sees this instead
# Her connect preferences
# Her skills and how proficient she is at each one

# She notices a link on the left hand side for her 'account settings'
# When she clicks on this she sees a page with:
# Her Username
# Her password (as bullets)
# Her email address



# MODERATORS


# Sam is a moderator.  She notices a link on the top menu to a moderators page.
# When she clicks on this page she sees





# TODO:
# Janine has asked Sam for an invitation to the site
# Sam clicks on the link to the 'moderators' page
# There she sees a form to invite new members
# She enters Janine's email address and clicks on the 'invite member' button

# Sam clicks on 'Logout' and is redirected to the login page

# Janine receives an email from the site  that contains a link to activate her account
# She clicks on it and is taken to a page where she can select a username and password
