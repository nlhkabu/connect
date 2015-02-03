from behave import *

# Common to this feature
@when('I visit the request account page')
def impl(context):
    context.browser.visit(context.server_url + 'accounts/request-invitation/')


# Unique to Scenario: User cancels attempt to request new account
@when('I cancel the request account form')
def impl(context):
    context.browser.find_by_css('.cancel').first.click()
