from connect.accounts.factories import AbuseReportFactory, AbuseWarningFactory
from behave import given, then, when
from common import DEFAULT_WAIT


# Background
@given('the second user has logged a complaint against the first')
def impl(context):
    AbuseReportFactory(logged_by=context.standard_user2,
                       logged_against=context.standard_user)

@given('the first standard user also has a prior warning')
def impl(context):
    warning = AbuseWarningFactory(logged_by=context.standard_user2,
                                  logged_against=context.standard_user,
                                  moderator=context.moderator)

@given('there has been a complaint logged against me')
def impl(context):
    report_3 = AbuseReportFactory(logged_by=context.standard_user,
                                  logged_against=context.moderator)


# Unique to Scenario: Visit abuse report page
@then('I see a list of abuse reports')
def impl(context):
    assert context.browser.is_element_present_by_css('.abuse-table')

@then('I see existing warnings')
def impl(context):
    assert context.browser.is_text_present('One prior warning', wait_time=DEFAULT_WAIT)

@then('I cannot see reports relating to myself')
def impl(context):
    assert context.browser.is_text_not_present('moderator@test.test')


# Unique to Scenario: View prior warnings
@when('I click on the prior warnings link')
def impl(context):
    context.browser.find_by_css('.show-warnings').click()

@then('I see the prior warnings modal, with information inside it')
def impl(context):
    assert context.browser.is_text_present('One prior warning for Standard User')
    assert context.browser.is_text_present('This is a complaint', wait_time=DEFAULT_WAIT) # Default from our factory
    assert context.browser.is_text_present('This is a formal warning', wait_time=DEFAULT_WAIT) # Default from our factory
    assert context.browser.is_text_present('by Another User')
    assert context.browser.is_text_present('by Moderator User')


# Unique to Scenario: Moderator submits data to the form
@when('I enter nothing in the comments field')
def impl(context):
    pass


# Unique to Scenario Outline: Moderator submits decision
@then('the report is removed from my abuse reports list')
def impl(context):
    pass

