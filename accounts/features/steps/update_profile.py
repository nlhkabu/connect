from behave import *


# Common to this feature
@when('I visit my profile page')
def impl(context):
    context.browser.visit(context.server_url + 'accounts/profile/')


# Common form fields
@when('I input "My link1" into the first anchor field')
def impl(context):
    context.browser.fill('link-0-anchor', 'My link1')

@when('I input "http://myurl1.com" into the first URL field')
def impl(context):
    context.browser.fill('link-0-url', 'http://myurl1.com')

@when('I input "My link2" into the second anchor field')
def impl(context):
    context.browser.fill('link-1-anchor', 'My link2')

@when('I input "http://myurl2.com" into the second URL field')
def impl(context):
    context.browser.fill('link-1-url', 'http://myurl2.com')

@when('I select "testskill1" for the first skill name field')
def impl(context):
    context.browser.find_by_xpath(
        "//select[@name='skill-0-skill']/option[text()='testskill1']").click()

@when('I select "Beginner" for the first skill proficiency field')
def impl(context):
    context.browser.find_by_xpath(
        "//select[@name='skill-0-proficiency']/option[text()='Beginner']").click()

@when('I select "testskill2" for the second skill name field')
def impl(context):
    context.browser.find_by_xpath(
        "//select[@name='skill-1-skill']/option[text()='testskill2']").click()

@when('I select "Expert" for the second skill proficiency field')
def impl(context):
    context.browser.find_by_xpath(
        "//select[@name='skill-1-proficiency']/option[text()='Expert']").click()


# Unique to Scenario: User views page
@then('I see the profile settings form')
def impl(context):
    assert context.browser.find_by_css('.profile-settings').visible

@then('the profile form is prepopulated with my data')
def impl(context):
    assert context.browser.find_by_name('first_name').value == 'Active'
    assert context.browser.find_by_name('last_name').value == 'User'


# Unique to Scenario Outline: User submits invalid data to update profile form
@when('there are two link formsets showing')
def impl(context):
    context.browser.find_link_by_text('add link').first.click()

@when('there are two skill formsets showing')
def impl(context):
    context.browser.find_link_by_text('add skill').first.click()

@when('I input "" into the first anchor field')
def impl(context):
    context.browser.fill('link-0-anchor', '')

@when('I input "" into the first URL field')
def impl(context):
    context.browser.fill('link-0-url', '')

@when('I input "My link1" into the second anchor field')
def impl(context):
    context.browser.fill('link-1-anchor', 'My link1')

@when('I input "http://myurl1.com" into the second URL field')
def impl(context):
    context.browser.fill('link-1-url', 'http://myurl1.com')

@when('I select "" for the first skill name field')
def impl(context):
    context.browser.select('skill-0-skill', '')

@when('I select "" for the first skill proficiency field')
def impl(context):
    context.browser.select('skill-0-proficiency', '')

@when('I select "testskill1" for the second skill name field')
def impl(context):
    context.browser.find_by_xpath(
        "//select[@name='skill-1-skill']/option[text()='testskill1']").click()

@then('I see "All links must have an anchor."')
def impl(context):
    assert context.browser.is_text_present("All links must have an anchor.")

@then('I see "All links must have a URL."')
def impl(context):
    assert context.browser.is_text_present("All links must have a URL.")

@then('I see "Links must have unique anchors and URLs."')
def impl(context):
    assert context.browser.is_text_present(
        "Links must have unique anchors and URLs.")

@then('I see "All skills must have a skill name."')
def impl(context):
    assert context.browser.is_text_present(
        "All skills must have a skill name.")

@then('I see "All skills must have a proficiency."')
def impl(context):
    assert context.browser.is_text_present(
        "All skills must have a proficiency.")

@then('I see "Each skill can only be entered once."')
def impl(context):
    assert context.browser.is_text_present(
        "Each skill can only be entered once.")


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


# Unique to Scenario: Update user's profile
@when('I input "my bio" into the bio field')
def impl(context):
    context.browser.fill('bio', 'my bio')

@when('I check "testrole1"')
def impl(context):
    # This is actually checking all the roles, but as there is only
    # one in the test DB, this is fine for our purposes.
    context.browser.check('roles')

@then('I see "Your example.com profile has been updated."')
def impl(context):
    assert context.browser.is_text_present("Your example.com profile has been updated.")
