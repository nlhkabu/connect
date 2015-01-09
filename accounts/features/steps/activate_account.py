from behave import *


# Common to this feature
@when('I visit my activation page (/7891011)')
def impl(context):
    #browser.visit(context.server_url + 'accounts/activate/7891011')
    pass

@when('I input "pass" into the confirm password field')
def impl(context):
    pass


# Unique to Scenario: Invited user visits page to activate account

@then('I see the activate account form')
def impl(context):
    pass

@then('the first name field is prepopulated with my first name')
def impl(context):
    pass

@then('the last name field is prepopulated with my last name')
def impl(context):
    pass


# Unique to Scenario Outline: Invited user submits invalid data to the activate account form
@when('I input "" into the confirm password field')
def impl(context):
    pass

@when('I input "notmatching" into the confirm password field')
def impl(context):
    pass

@then('I see "Your passwords do not match. Please try again."')
def impl(context):
    pass


# Unique to Scenario: Invited user activates their account
@then('I see a welcome modal')
def impl(context):
    pass


# Unique to Scenario: Active user revisits page to activate account
@when('I visit my activation page (/123456)')
def impl(context):
    pass

@then('I see "We\'re sorry, this activation token has already been used."')
def impl(context):
    pass
