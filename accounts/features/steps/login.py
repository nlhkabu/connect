from behave import *

# Common to this feature
@when('I visit the login page')
def impl(context):
    context.browser.visit(context.server_url + 'accounts/login/')


# Unique to Scenario Outline: Invalid login
@then('I see "Your email and password didn\'t match. Please try again."')
def impl(context):
    pass
