from behave import then, when
from common import DEFAULT_WAIT


# Unique to Scenario: Moderator does not confirm revocation
@when('I do not check the confirmation box')
def impl(context):
    pass

# Unique to Scenario: Moderator confirms revocation
@when('I check the confirmation box')
def impl(context):
    context.browser.check('confirm')

@then('the invited user has been removed from my pending invitations list')
def impl(context):
    assert context.browser.is_text_not_present('invited.user@test.test',
                                               wait_time=DEFAULT_WAIT)
