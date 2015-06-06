from behave import *


# Unique to Scenario: User submits valid data
@when('I close my account')
def impl(context):
    context.execute_steps('''
        when I enter "pass" into the "password" field
        when I submit the form
    ''')

@then('I am redirected to a confirmation page')
def impl(context):
    assert 'Account Closed' in context.browser.title
