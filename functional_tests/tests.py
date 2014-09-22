#from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.contrib.auth import get_user_model


User = get_user_model()


# test what happens from the users' points of view
# ================================================

class UserVisitTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()


    def test_layout_and_styling(self):
        # Sam goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # TODO: Test layout here
        pass


    #~def test_can_login_via_login_page(self):
#~
        #~sam = User.objects.create_user(email="sam@example.com",
                                       #~password="pass")
#~
        #~# Sam visits the connect homepage and sees that she needs to login
        #~self.browser.get(self.live_server_url)
        #~self.assertIn('Login', self.browser.title)
#~
        #~# There she sees a login form with email address (username) and password fields
        #~input_email = self.browser.find_element_by_id('id_username')
        #~input_password = self.browser.find_element_by_id('id_password')
#~
        #~# Sam enters her email address and an incorrect password
        #~input_email.send_keys('sam@example.com')
        #~input_password.send_keys('wrongpass')
        #~input_password.send_keys(Keys.ENTER)
#~
        #~# But is told that the email address and password do not match
        #~header_content = self.browser.find_element_by_tag_name('header').text
        #~self.assertIn("Your email and password didn't match", header_content)
#~
        #~# She tries again, this time with the correct password
        #~input_password = self.browser.find_element_by_id('id_password')
#~
        #~input_password.send_keys('pass')
        #~input_password.send_keys(Keys.ENTER)
#~
        #~# Success! She is redirected to the connect dashboard
        #~self.assertIn('Dashboard', self.browser.title)


# There she sees:

# A card for each user registered on the site, with:
# User name
# User gravatar (if they have one)
# User roles
# User skills (and their proficiency)
# User bio
# User links
# Link to report this user for abuse

# Sam notices a form on the page where she can 'Refine' her search

## SKILLS/INTERESTS

# When she selects 'Django' and clicks on 'submit', she notices that
# the users she sees all have the skill 'Django'

# When she selects 'Django' and 'Game Development' she sees all of
# the users with the skills 'Django' OR 'Game Development'

## CONNECT PREFERENCES

# Sam also notices that she can filter results by their preferred roles.
# She selects 'Mentor' to see all of the users who have the role 'mentor'.
# Likewise, when she selects 'Mentor' and 'Mentee' she sees all of the users
# with the roles 'Mentor' OR 'Game Development'

# Sam notices that she can filter users by BOTH skill/interest & preferred role.
# She is looking for a Django mentor, so selects 'Django' and 'Mentor'
# All of the users listed in the results have the skill 'Django' and the
# role 'Mentor'.

# Sam is also making a Python game and is looking for users to join her.
# She selects 'Game Development' and 'Coding Buddy', but there is nobody in
# the system who matches this search, so she sees a 'no results' message.
