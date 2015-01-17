from behave import *

# Common to this feature
@when('I visit the reset password page')
def impl(context):
    context.browser.visit(context.server_url + 'accounts/password/reset/')


# Unique to Scenario Outline: User requests password reset
@when('I input "not.a.user@test.test" into the email field')
def impl(context):
    context.browser.fill('email', 'not.a.user@test.test')


# Unique to Scenario: User requests a new account
@then('I am taken to a confirmation page that says "Please check your email"')
def impl(context):
    assert context.browser.is_text_present('Please check your email')
