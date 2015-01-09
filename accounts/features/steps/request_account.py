from behave import *

# Common to this feature
@when('I visit the request account page')
def impl(context):
    pass

@when('I input "comment" into the comments field')
def impl(context):
    pass


# Unique to Scenario Outline: User submits invalid data to the request account form
@when('I input "request.account@test.test" into the email field')
def impl(context):
    pass

@when('I input "" into the comments field')
def impl(context):
    pass


# Unique to Scenario: User cancels attempt to request new account
@when('I cancel the request account form')
def impl(context):
    pass

# Unique to Scenario: User requests a new account
@then('I see "Your request for an account has been sent"')
def impl(context):
    pass
