from behave import *

# Common to this feature
@when('I visit the reset password page')
def impl(context):
    pass


# Unique to Scenario Outline: User requests password reset
@when('I input "not.a.user@test.test" into the email field')
def impl(context):
    pass


# Unique to Scenario: User requests a new account
@then('I am taken to a confirmation page that says "Please check your email"')
def impl(context):
    pass
