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

        sam = User.objects.create_user(username="sam",
                                       email="sam@example.com",
                                       password="pass")

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
        header_content = self.browser.find_element_by_tag_name('header').text
        self.assertIn("Your username and password didn't match", header_content)

        # She tries again, this time with the correct password
        input_password = self.browser.find_element_by_id('id_password')

        input_password.send_keys('pass')
        input_password.send_keys(Keys.ENTER)

        # Success! She is redirected to the connect dashboard
        self.assertIn('Dashboard', self.browser.title)


# There she sees:

# A card for each member registered on the site, with:
# Member name
# Member gravatar (if they have one)
# Member connect preferences
# Member skills (and their proficiency)
# Member bio
# Member links

# Sam notices a form on the page where she can 'Refine' her search

## SKILLS/INTERESTS

# When she selects 'Django' and clicks on 'submit', she notices that
# the members she sees all have the skill 'Django'

# When she selects 'Django' and 'Game Development' she sees all of
# the members with the skills 'Django' OR 'Game Development'

## CONNECT PREFERENCES

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

## MY ACCOUNT

# Sam notices a link at the top right called 'My Account'.
# When she clicks on the link, she is taken to a page where she sees her
# 'profile' settings.

# Here she sees:
# Her First Name
# Her Last Name
# Her Biography
# Her connect preferences
# Her skills and how proficient she is at each one
# Her links

# Sam updates her first name and clicks 'save preferences'
# When the page reloads, her updated name appears.

# She does the same for her last name, bio and connect preferences.

# Sam decides that she doesn't want the connect community to know her last name.
# So she makes this field empty and saves her preferences.

# When the page reloads, she can see that no last name is registered on her account.
# She does the same for her biography.

# Then she tries to remove her first name, but is prompted by a message telling
# her that this is a required field.

## SKILLS

# Sam looks at her skills and realises that 'Django' is listed as 'beginner'
# - but she thinks she is better than that

# She selects 'intermediate' next to the 'Django' form
# When the page reloads, this skill has been saved

# She adds another skill - game development - beginner.
# When the page reloads, this skill has been saved

# She notices that she has previously nominated 'scienfic python' as a skill
# by mistake.

# She clicks on the 'remove' button and it dissapears.  When she saves
# the form, it is perminately removed from her skills list.

## CUSTOM VALIDATION

# She decides to add the skill 'Django' - but an error message appears telling her
# that she has already registered 'Django' as a skill

# She notices that 'Public Speaking' is in the list, so she selects this
# and clicks save.

# A validation message appears telling her that she must specify a proficieny.

# She selects 'beginner'.  Then she accidently changes 'Public Speaking' to blank.

# A validation message appears telling her that she must specify a skill

# Finally, she selects 'Public Speaking' making sure that 'beginner' is still selected.
# This time it saves as expected

## LINKS

# Sam looks at her links and decides to change her link labelled with 'Facebook'
# to say 'My Facebook Page'

# She also notices that 'facebook' is misspelt in the url so corrects it.

# When she saves the form, the link updates as expected

# Sam notices a youtube link for an account that is no longer active.
# She clicks on the 'remove' button and it dissapears.  When she saves the
# form, it is perminately removed from her links list.

# She adds another link 'GitHub', 'http://github.com/sam'.
# Then she clicks on the 'add another' button.
# A new form appears and she inputs 'Bitbucket' and 'http://bitbucket.org/sam
# When she saves the form, both new links stay on her list.

## CUSTOM VALIDATION

# Sam has two facebook accounts.
# She adds another link - 'My Facebook Page' - 'http://facebook.com/samssecondpage

# When she submits the form a validation message appears telling her that
# the link anchor text must be unique.

# She changes the anchor to 'My Other Facebook Page' and the form submits as
# expected.

# Sam wants to add her second github account.
# She adds another link - 'My Second Github account', 'http://github.com/sam'

# Whoops!  A validation message appears telling her that URLs must be unique.
# She realises what she has done and changes the URL to 'http://github.com/samssecondaccount'

# Sam enters a new link for her personal homepage - 'http://samshomepage.com'
# and submits the form

# A validation message appears telling her that she needs to specify the
# anchor text

# She enters - 'My homepage' but accidently deletes 'http://samshomepage.com'

# A validation message appears telling her that she needs to specify the URL

# Finally, she re-enters 'http://samshomepage.com' next to 'My homepage'
# The form submits as expected.


## ACCOUNT SETTINGS
# She notices a link on the left hand side for her 'account settings'

# When she clicks on this she sees a page with:
# Her Username
# Her password (as bullets)
# Her email address


