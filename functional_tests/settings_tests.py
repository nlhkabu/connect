from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.contrib.auth.models import User

# test what happens from the users' points of view
# ================================================

## MY ACCOUNT

# Greg logs into connect to change some of his preferences.

# Greg notices a link at the top right called 'My Account'.
# When he clicks on the link, he is taken to a page whise he sees his
# 'profile' settings.

# Here he sees:
# His First Name
# His Last Name
# His Biography
# His connect preferences
# His skills and how proficient he is at each one
# His links

# Greg updates his first name and clicks 'save preferences'
# When the page reloads, his updated name appears.

# He does the same for his last name, bio and connect preferences.

# Greg decides that he doesn't want the connect community to see his biography.
# So he makes this field empty and saves his preferences.

# When the page reloads, he can see that no biography is registered on his account.

# Then he tries to remove his first name and last name, but is prompted by a
# message telling him that these fields are required.

## SKILLS

# Greg looks at his skills and realises that 'Django' is listed as 'beginner'
# - but he thinks he is better than that

# He selects 'intermediate' next to the 'Django' form
# When the page reloads, this skill has been saved

# He adds another skill - game development - beginner.
# When the page reloads, this skill has been saved

# He notices that he has previously nominated 'scienfic python' as a skill
# by mistake.

# He clicks on the 'remove' button and it dissapears.  When he saves
# the form, it is perminately removed from his skills list.

## CUSTOM VALIDATION

# He decides to add the skill 'Django' - but an error message appears telling his
# that he has already registered 'Django' as a skill

# He notices that 'Public Speaking' is in the list, so he selects this
# and clicks save.

# A validation message appears telling him that he must specify a proficieny.

# He selects 'beginner'.  Then he accidently changes 'Public Speaking' to blank.

# A validation message appears telling his that he must specify a skill

# Finally, he selects 'Public Speaking' making sure that 'beginner' is still selected.
# This time it saves as expected

## LINKS

# Greg looks at his links and decides to change his link labelled with 'Facebook'
# to say 'My Facebook Page'

# He also notices that 'facebook' is misspelt in the url - so corrects it.
# When he saves the form, the link updates as expected

# Greg notices a youtube link for an account that is no longer active.
# He clicks on the 'remove' button and it dissapears.  When he saves the
# form, it is perminately removed from his links list.

# He adds another link 'GitHub', 'http://github.com/Greg'.
# Then he clicks on the 'add another' button.
# A new form appears and he inputs 'Bitbucket' and 'http://bitbucket.org/greg
# When he saves the form, both new links stay on his list.

## CUSTOM VALIDATION

# Greg has two facebook accounts.
# He adds another link - 'My Facebook Page' - 'http://facebook.com/gregssecondpage

# When he submits the form a validation message appears telling him that
# the link anchor text must be unique.

# He changes the anchor to 'My Other Facebook Page' and the form submits as
# expected.

# Greg wants to add his second github account.
# He adds anothis link - 'My Second Github account', 'http://github.com/greg'

# Whoops!  A validation message appears telling his that URLs must be unique.
# He realises what he has done and changes the URL to 'http://github.com/gregssecondaccount'

# Greg enters a new link for his personal homepage - 'http://gregshomepage.com'
# and submits the form

# A validation message appears telling his that he needs to specify the
# anchor text

# He enters - 'My homepage' but accidently deletes 'http://gregshomepage.com'

# A validation message appears telling his that he needs to specify the URL

# Finally, he re-enters 'http://gregshomepage.com' next to 'My homepage'
# The form submits as expected.


## ACCOUNT SETTINGS

# Greg notices a link on the left hand side for his 'account settings'

# When he clicks on this he sees a page with:
# His Username
# His email address
# Two fields to change his password

# Greg decides to change his username from 'greggy' to just 'greg'
# but when he does so, he is told that there is already a user with the username
# 'greg' registered.

# He decides instead to delete his username altogether.
# but an error (telling him that a username is required) prevents him from doing so.

# Finally, he successfully changes his username to 'greggo'

# Greg tries to remove his email address.  But is told that this is a required field.
# So he decides instead to change it to his partner's email - sam@gmail.com

# What he doesn't know - Sam already has a connect account set up...
# So Greg is faced with an error message telling him that he can't use that
# email address, as it is already registered in the connect system.

# Not having much luck - Greg finally decides to change his email address
# to a new gmail account - gregconnect@gmail.com.
# Finally he is successful.

# While he is here, Greg decides to change his password.
# Greg wants to change his password to 'xyz123', but he has clumsy fingers...
# and accidently inputs 'xyz122' into the 'confirm password' field.

# An error message appears telling him that the password fields must match.
# Realising his mistake, Greg makes both fields 'xyz123' and successfully
# changes his password.

# Satisfied, he logs out.
