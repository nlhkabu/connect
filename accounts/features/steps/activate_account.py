from behave import *


# Common to this feature
@when('I visit my activation page (/7891011)')
def impl(context):
    context.browser.visit(context.server_url + 'accounts/activate/7891011')

@when('I input "pass" into the confirm password field')
def impl(context):
    context.browser.fill('confirm_password', 'pass')


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


# Unique to Scenario Outline: Invited user submits
# invalid data to the activate account form
@when('I input "" into the confirm password field')
def impl(context):
    context.browser.fill('confirm_password', '')

@when('I input "notmatching" into the confirm password field')
def impl(context):
    context.browser.fill('confirm_password', 'notmatching')

@then('I see "Your passwords do not match. Please try again."')
def impl(context):
    assert context.browser.is_text_present(
        'Your passwords do not match. Please try again.')


# Unique to Scenario: Invited user activates their account
@then('I see a welcome modal')
def impl(context):
    assert context.browser.find_by_css('.welcome-message').visible


# Unique to Scenario: Active user revisits page to activate account
@when('I visit my activation page (/123456)')
def impl(context):
    context.browser.visit(context.server_url + 'accounts/activate/123456')

@then('I see "We\'re sorry, this activation token has already been used."')
def impl(context):
    assert context.browser.is_text_present(
        "We're sorry, this activation token has already been used.")
