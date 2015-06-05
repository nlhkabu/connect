from behave import *


# Unique to Scenario: Clicking on 'resend invitation' launches modal
@then('the invited user\'s email is prepopulated in the form')
def impl(context):
    email_field = context.browser.find_by_css('.reinvite-member-form #id_email')
    assert email_field.value == 'invited.user@test.test'
