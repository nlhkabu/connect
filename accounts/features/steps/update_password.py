from behave import *

# Common to this feature
@when('I visit the update password page')
def impl(context):
    context.browser.visit(context.server_url + 'accounts/update/password/')

@when('I input "pass" into the new password field')
def impl(context):
    context.browser.fill('new_password', 'pass')

@when('I input "pass" into the current password field')
def impl(context):
    context.browser.fill('current_password', 'pass')


# Unique to Scenario: User views page
@then('I see the update password form')
def impl(context):
    assert context.browser.find_by_css('.update-password').visible


# Unique to Scenario Outline: User submits invalid data to the
# update password form
@when('I input "" into the new password field')
def impl(context):
    context.browser.fill('new_password', '')

@when('I input "" into the current password field')
def impl(context):
    context.browser.fill('current_password', '')

@when('I input "wrongpass" into the current password field')
def impl(context):
    context.browser.fill('current_password', 'wrongpass')


# Unique to Scenario: User updates their password
@then('I see "Your example.com password has been updated."')
def impl(context):
    assert context.browser.is_text_present(
        "Your example.com password has been updated.")

