from behave import *


# Unique to Scenario: User logs out
@when('I click on the logout link')
def impl(context):
    context.browser.find_link_by_text('Logout').first.click()

@then('I am no longer authenticated')
def impl(context):
    pass
