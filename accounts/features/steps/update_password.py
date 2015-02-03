from behave import *

# Common to this feature
@when('I visit the update password page')
def impl(context):
    context.browser.visit(context.server_url + 'accounts/update/password/')

# Unique to Scenario: User views page
@then('I see the update password form')
def impl(context):
    assert context.browser.find_by_css('.update-password').visible

