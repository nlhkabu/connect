from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.contrib.auth import get_user_model


User = get_user_model()


# Inviting new users
# ==================

# Janine is a connect moderator and has been asked by a friend for an
# invitation.

# When she logs into connect, she sees a 'moderators' link in the menu.
# She clicks on the link and is taken to a page with a form for inviting new users

# She also sees a list of the user's she has already invited to the system,
# but who have not activated their account.

# She enters the details of her friend who she wants to invite:
# Lily
# Ivanov
# lily@gmail.com

# When she submits the form, Lily now appears in her 'pending users' list.
# Lily's listing also includes the date and time Janine invited her
# and the options to resend or revoke the invitation.

# Alex has also asked Janine for an invitation

# Alex's has given Janine her details:
# Alex
# Chakravarty
# alexrocks@gmail.com

# ... but whoops!  Janine enters these without a first name!
# An error message is raised.

# Janine fixes this, but accidently deletes Alex's last name and email address!
# An error message is raised for each field.

# Frustrated and confused, Janine finally enters all of Alex's details.
# An error message appears telling her that Alex's email address is already registered.

# Janine gives up, logs out and goes to get herself a glass of wine.


# A little tipsier and significantly more relaxed, Janine logs on again.
# She noticed earlier that Riley had not activated his account - perhaps she
# put in the wrong email address.

# Yes! She did.  She resends Riley's invitation, this time with riley@gmail.com
# as the email address.

# An error message appears telling her that this email address is already in the
# system.  Riley must have asked another moderator for an invitation.

# As this invitation is no longer relevant, Janine decides to revoke it (and remove)
# it from her pending user's list.

# She clicks on 'revoke invitation' but is asked to provide a comment.
# She fills the comment box in and Riley's invitation is removed from the list.

# Janine notices that Kelly has not activated her account.
# Janine succesfully resents an invitation to Kelly.

# Satisfied with her activity, Janine views the moderation logs.
# There she sees:

# - A log of sending Lily's invitation
# - A log of revoking Riley's invitation
# - A log of resending Kelly's invitation

# Janine logs out


# User Applications
# =================

# Abby applies for a connect usership at accounts/request-invitation
# At first she accidently tries to submit the form without any of the fields filled
# but is met with an error message for each field telling her that she must
# supply information for each field.

# Trying again, she enters a shared work email: myworkplace@google.com
# but is told that this email address is already in the Connect system.

# Finally she uses her own email address: abby@gmail.com and is redirected
# to a success message


# Chris applies for a connect usershup at accounts/request-invitation - filling
# in all fields correctly.

# He is redirected to a success message.


# Janine logs into her connect account and navigates to /moderation/review-usership-applications

# She notices two applications listed - one for Abby and one for Chris.
# Each application includes:
# - Name
# - Email Address
# - Date and time the invitation was requested
# - Comments submitted by the applicant
# - A moderation form allowing the applicant to be approved or rejected

# Janine finds Abby's application comments inappropriate and decides to reject
# her application on these grounds.

# She selects 'Rejected' on the dropdown and submits the form.
# An error message appears asking her to fill out the comments section.

# She fills out a comment and Abby is removed from the applications list.

# Janine reviews Chris' application and decides to send him a connect invitation.
# She selects 'Approved' on the dropdown and makes a comment.
# After submitting the form, Chris' application is removed from the list.

# Janine navigates to the moderation logs and notices a log for each decision.
# Janine logs out.


# Abuse Reports
# =============

# Chris has been contacted by another user (Jane) who is interested in catching up
# for a coffee.

# Chris clicks on the 'report abuse' button on Jane's profile.
# He tries to submit the form without a comment, but an error message appears
# asking him to provide details about why he thinks that Jane's behaviour is
# inappropriate.

# Chris fills out this field and submits the report - a confirmation message appears.

# Chris has been contacted by another user (Sally) who is using connect
# as a recruitment platform.

# Chris follows the same process to report Sally.

# Chris logs out.


# Janine logs into her connect account and navigates to moderation/review-abuse-reports

# She sees Chris' abuse reports, they includes:

# The name of the person reported (in this case Jane or Sally)
# Chris' full name
# The date and time the report was logged
# Chris' complaint.
# A form to dismiss the report, issue a warning or ban the person reported.

# Janine CANNOT see an earlier abuse report logged against her.

# Janine decides that Jane's behaviour is within the community
# guidelines, so she decides to dismisses the abuse report.

# She selects 'Dismiss Report' on the dropdown, but forgets to write a comment.
# An error message appears asking her to provide a comment.

# She does so, and successfully submits the form, removing the complaint against
# Jane from her list.

# Whilst Sally's behaviour does not technically breech of the community guidelines,
# Janine wants to deter recruiters from spamming the community.
# She decides to issue a warning to Sally.

# Janine selects 'Warn Abuser' and provides a comment.
# The complain against Sally is removed from her list.

# Janine navigates to the logs page and sees a log for each of her actions.

# Janine logs out.


# Susan has been receiving recruitment spam from Sally and subsequently
# logs an abuse report against her.

# When Janine logs in the next time, she notices a new report against Sally,

# This time, however, there is information about the warning previously issued
# to Sally.

# Reviewing this complaint, and given the previous warning, Janine decides to ban
# Sally and fills out the form accordingly.

# When she navigates to the moderation logs, she notices her decision is
# logged there.

# When she navigates to the homepage of the app, Sally is no longer listed as
# a user.

# Satisfied, Janine logs out.


# Moderation Logs
# ===============

# Bill logs into connect and navigates to the moderation logs.
# He sees a list of all moderation events, with those last added at the top of the list.

# Bill filters the logs by 'invited'
# The logs are filtered correctly.

# Bill filters the logs by those recorded today
# The logs are filtered correctly.

# Bill filters the logs by those recorded yesterday
# The logs are filtered correctly.

# Bill filters the logs by those recorded in the last seven days
# The logs are filtered correctly.

# Bill filters the logs by 'custom date range' selecting those recorded between four days ago and today
# The logs are filtered correctly.

# Bill filters the logs by 'custom date range', but does not select a start date
# Bill sees a message asking him to specify a start and end date.  The logs remain unfiltered.

# Bill filters the logs by 'custom date range', but does not select an end date
# Bill sees a message asking him to specify a start and end date.  The logs remain unfiltered.

# Bill filters the logs by 'Invited' and 'today'
# The logs are filtered correctly.

# Finally, bill selects 'all' on both dropdowns
# Again, he sees a list of all moderation events.


