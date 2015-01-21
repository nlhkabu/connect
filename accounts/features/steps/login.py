from behave import *

# Common to this feature
@when('I visit the login page')
def impl(context):
    context.browser.visit(context.server_url + 'accounts/login/')

@when('I input "" into the username/email field')
def impl(context):
    context.browser.fill('username', '')

@when('I input "active.user@test.test" into the username/email field')
def impl(context):
    context.browser.fill('username', 'active.user@test.test')

@when('I input "invalidemail" into the username/email field')
def impl(context):
    context.browser.fill('username', 'invalidemail')


# Unique to Scenario Outline: Invalid login
@then('I see "Your email and password didn\'t match. Please try again."')
def impl(context):
    assert context.browser.is_text_present(
        "Your email and password didn't match. Please try again.")
