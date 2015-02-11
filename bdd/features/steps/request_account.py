from behave import *


# Unique to Scenario: User cancels attempt to request new account
@when('I cancel the request account form')
def impl(context):
    context.browser.find_by_css('.cancel').first.click()
