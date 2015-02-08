from behave import *


# Unique to Scenario: User views page
@then('I see the update email form, prepopulated with my email')
def impl(context):
    assert context.browser.find_by_css('.update-email').visible
    assert context.browser.find_by_name('email').value == 'standard.user@test.test'


