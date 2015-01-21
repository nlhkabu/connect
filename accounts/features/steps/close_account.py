from behave import *


# Common to this feature
@given('I am an authenticated user wanting to close my account')
def impl(context):
    pass

@when('I visit the close account page')
def impl(context):
    context.browser.visit(context.server_url + 'accounts/close/')


# Unique to Scenario: User views page
@then('I see the close account form')
def impl(context):
    assert context.browser.find_by_css('.close-account').visible


# Unique to Scenario: User submits valid data
@then('I am redirected to a confirmation page')
def impl(context):
    assert b'Account Closed' in context.browser.title
