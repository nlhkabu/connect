from behave import *


# Common to this feature
@when('I visit my activation page "{url}"')
def impl(context, url):
    context.browser.visit(context.server_url + 'accounts/activate/' + url )


# Unique to Scenario: Invited user visits page to activate account
@then('I see the activate account form')
def impl(context):
    assert context.browser.find_by_css('.activate-account').visible

@then('the first name field is prepopulated with my first name')
def impl(context):
    assert context.browser.find_by_name('first_name').value == 'Inactive'

@then('the last name field is prepopulated with my last name')
def impl(context):
    assert context.browser.find_by_name('last_name').value == 'User'


# Unique to Scenario: Invited user activates their account
@then('I see a welcome modal')
def impl(context):
    assert context.browser.find_by_css('.welcome-message').visible

