from behave import *


# Common to this feature
@when('I visit my activation page "{url}"')
def impl(context, url):
    context.browser.visit(context.config.server_url + '/accounts/activate/' + url )


# Unique to Scenario: Invited user visits page to activate account
@then('I see the activate account form, prepopulated with my data')
def impl(context):
    assert context.browser.find_by_css('.activate-account').visible
    assert context.browser.find_by_name('full_name').value == 'Inactive User'


# Unique to Scenario: Invited user activates their account
@when('I activate my account')
def impl(context):
    context.execute_steps('''
        when I enter "First Last" into the "full name" field
         and I enter "pass" into the "password" field
         and I enter "pass" into the "confirm password" field
         and I submit the form
    ''')


@then('I see a welcome modal')
def impl(context):
    assert context.browser.find_by_css('.welcome-message').visible

