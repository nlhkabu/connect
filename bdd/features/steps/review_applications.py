from behave import *


# Common
@given('I have launched the "{modal_name}" modal')
def impl(context, modal_name):
    modal_name = modal_name.title()
    context.execute_steps('when I visit the "review applications" page')
    context.browser.click_link_by_text(modal_name)

# Unique to Scenario: View applications
@then('I see a list of pending applications')
def impl(context):
    assert context.browser.is_element_present_by_css('.review-app-table')
    assert context.browser.is_text_present('Pending', wait_time=10)
    assert context.browser.is_text_present('Approval', wait_time=10)
    assert context.browser.is_text_present('pending.approval@test.test', wait_time=10)


# Unique to Scenario Outline: Launch modal
@then('a modal containing a "{form_name}" pops up')
def impl(context, form_name):
    form_name = form_name.lower().replace(" ", "-") + '-form'
    context.browser.is_element_present_by_css(form_name, wait_time=10)

@when('I click on "{link_text}"')
def impl(context, link_text):
    context.browser.click_link_by_text(link_text)


# Unique to Scenario: Close review application modal
@when('I click on the close button')
def impl(context):
    context.browser.find_by_css('.ui-dialog-titlebar-close').first.click()

@then('the modal closes')
def impl(context):
    context.browser.is_element_not_present_by_css('.ui-dialog')


# Unique to Scenario Outline: Moderator submits decision
@then('"{user}" is removed from my list')
def impl(context, user):
    assert context.browser.is_text_not_present(user)

