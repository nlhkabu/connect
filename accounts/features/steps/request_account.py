from behave import *

# Common to this feature
@when('I visit the request account page')
def impl(context):
    context.browser.visit(context.server_url + 'accounts/request-invitation/')

@when('I input "comment" into the comments field')
def impl(context):
    context.browser.fill('comments', 'comment')


# Unique to Scenario Outline: User submits invalid data to the request account form
@when('I input "request.account@test.test" into the email field')
def impl(context):
    context.browser.fill('email', 'request.account@test.test')

@when('I input "" into the comments field')
def impl(context):
    context.browser.fill('comments', '')


# Unique to Scenario: User cancels attempt to request new account
@when('I cancel the request account form')
def impl(context):
    context.browser.find_by_css('.cancel').first.click()

# Unique to Scenario: User requests a new account
@then('I see "Your request for an account has been sent"')
def impl(context):
    assert context.browser.is_text_present(
        'Your request for an account has been sent')
