from behave import *


# Unique to Scenario: User logs out
@when('I click on the logout link')
def impl(context):
    pass

@then('I am no longer authenticated')
def impl(context):
    pass
