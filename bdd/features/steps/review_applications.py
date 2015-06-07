from behave import then
from common import DEFAULT_WAIT


# Unique to Scenario: View applications
@then('I see a list of pending applications')
def impl(context):
    assert context.browser.is_element_present_by_css('.review-app-table')
    assert context.browser.is_text_present('Pending', wait_time=DEFAULT_WAIT)
    assert context.browser.is_text_present('Approval', wait_time=DEFAULT_WAIT)
    assert context.browser.is_text_present('pending.approval@test.test', wait_time=DEFAULT_WAIT)


# Unique to Scenario Outline: Moderator submits decision
@then('"{user}" is removed from my list')
def impl(context, user):
    assert context.browser.is_text_not_present(user)

