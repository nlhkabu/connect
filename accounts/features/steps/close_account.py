from behave import *


# Common to this feature
@when('I visit the close account page')
def impl(context):
    pass

@when('I submit the close account form')
def impl(context):
    pass


# Unique to Scenario: User views page
@then('I see the close account form')
def impl(context):
    pass


# Unique to Scenario: User submits valid data
@then('I am redirected to a confirmation page')
def impl(context):
    pass
