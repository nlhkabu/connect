from behave import *


# Common to this feature
@when('I visit the close account page')
def impl(context):
    context.browser.visit(context.server_url + 'accounts/close/')


# Unique to Scenario: User submits valid data
@when('I close my account')
def impl(context):
    context.execute_steps('''
        when I enter "pass" into the "password" field
        when I submit the form
    ''')

@then('I am redirected to a confirmation page')
def impl(context):
    assert b'Account Closed' in context.browser.title
