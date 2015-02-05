from behave import *


# Common to this feature
@when('I visit my profile page')
def impl(context):
    context.browser.visit(context.server_url + 'accounts/profile/')


# Unique to Scenario: User views page
@then('I see the profile settings form, prepopulated with my data')
def impl(context):
    assert context.browser.find_by_css('.profile-settings').visible
    assert context.browser.find_by_name('first_name').value == 'Active'
    assert context.browser.find_by_name('last_name').value == 'User'


# Unique to Scenario: Biography field expands
@when('I add more than three lines to the biography field')
def impl(context):
    context.bio_height = context.browser.driver.find_element_by_name('bio').size['height']
    context.browser.fill('bio', 'line1\n\nline2\nline3\nline4\nline5\nline6\n')

@then('the field grows to accommodate the text')
def impl(context):
    new_height = context.browser.driver.find_element_by_name('bio').size['height']
    assert new_height > context.bio_height


# Unique to Scenario: Remove a form from the skills list
@when('I click on remove next to the first skill form')
def impl(context):
    context.browser.find_by_css('.delete-skill').first.click()

@then('the first skill formset is removed from the list')
def impl(context):
    assert context.browser.is_element_not_present_by_name('skill-0-skill')
    assert context.browser.is_element_not_present_by_name('skill-0-proficiency')


# Unique to Scenario: Add another form to the skills list
@when('I click on add skill')
def impl(context):
    context.browser.find_link_by_text('add skill').first.click()

@then('another skill formset is added to the bottom of the form')
def impl(context):
    assert context.browser.is_element_present_by_name('skill-1-skill')
    assert context.browser.is_element_present_by_name('skill-1-proficiency')


# Unique to Scenario: Remove a form form the links list
@when('I click on remove next to the first link form')
def impl(context):
    context.browser.find_by_css('.delete-link').first.click()

@then('the first link formset is removed from the list')
def impl(context):
    assert context.browser.is_element_not_present_by_name('link-0-anchor')
    assert context.browser.is_element_not_present_by_name('link-0-url')


# Unique to Scenario: Add another form to the links list
@when('I click on add link')
def impl(context):
    context.browser.find_link_by_text('add link').first.click()

@then('another link formset is added to the bottom of the form')
def impl(context):
    assert context.browser.is_element_present_by_name('link-1-anchor')
    assert context.browser.is_element_present_by_name('link-1-url')


# Unique to Scenario Outline: User submits update profile form
@when('there are two link formsets showing')
def impl(context):
    context.execute_steps('when I click on add link')

@when('there are two skill formsets showing')
def impl(context):
    context.execute_steps('when I click on add skill')

@when('I select "{selection}" from the "{field_name}" dropdown')
def impl(context, selection, field_name):

    SKILL_FORMSET = {
        'first skill name': 'skill-0-skill',
        'first skill proficiency': 'skill-0-proficiency',
        'second skill name': 'skill-1-skill',
        'second skill proficiency': 'skill-1-proficiency',
    }

    field_name = SKILL_FORMSET[field_name]

    path = "//select[@name='{}']/option[text()='{}']".format(field_name,
                                                             selection)

    context.browser.find_by_xpath(path).click()
