# test what happens from the users' points of view
# ================================================

# Sam visits the connect homepage and sees a login form with username and password fields

# She enters her username and password
# But is told that the username and password do not match

# She tries again, this time she gets it right and is taken to her dashboard

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




# Her Name
# Her Biography
# Her gravatar image (if she has one)
# OR if she has uploaded a different image, she sees this instead
# Her connect preferences
# Her skills and how proficient she is at each one


# TODO:
# Sam is a moderator  - Janine has asked her for an invitation to the site
# Sam clicks on the link to the 'moderators' page
# There she sees a form to invite new members
# She enters Janine's email address and clicks on the 'invite member' button

# Sam clicks on 'Logout' and is redirected to the login page

# Janine receives an email from the site  that contains a link to activate her account
# She clicks on it and is taken to a page where she can select a username and password
