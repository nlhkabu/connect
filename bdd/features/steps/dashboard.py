from behave import *
from accounts.factories import UserFactory, UserSkillFactory
from accounts.models import Role, Skill

# Background
@given('the following users exist')
def impl(context):

    role1 = Role.objects.get(name='role1')
    role2 = Role.objects.get(name='role2')

    skill1 = Skill.objects.get(name='skill1')
    skill2 = Skill.objects.get(name='skill2')

    user1 = UserFactory(email='email1@test.test')
    user1_skill1 = UserSkillFactory(user=user1, skill=skill1)
    user1_skill2 = UserSkillFactory(user=user1, skill=skill2)

    user2 = UserFactory(email='email2@test.test', roles=[role1, role2])

    user3 = UserFactory(email='email3@test.test', roles=[role1,])
    user3_skill1 = UserSkillFactory(user=user3, skill=skill1)

    user4 = UserFactory(email='email4@test.test')
    user4_skill2 = UserSkillFactory(user=user4, skill=skill2)

    user5 = UserFactory(email='email5@test.test', roles=[role2,])
    user5_skill1 = UserSkillFactory(user=user5, skill=skill1)
    user5_skill2 = UserSkillFactory(user=user5, skill=skill2)

    user6 = UserFactory(email='email6@test.test', roles=[role1, role2])
    user6_skill1 = UserSkillFactory(user=user6, skill=skill1)
    user6_skill2 = UserSkillFactory(user=user6, skill=skill2)

    user7 = UserFactory(email='email7@test.test', roles=[role1,])
    user7_skill2 = UserSkillFactory(user=user7, skill=skill2)


# Unique to Scenario: User views dashboard
@then('I see the application name in the banner')
def impl(context):
    assert context.browser.is_text_present('example.com')

@then('I see a list of members, including myself')
def impl(context):

    members = context.browser.find_by_css('.user-card')
    assert len(members) == 8


# Unique to Scenario Outline: Filter members
@when('I filter members by "{checked}"')
def impl(context, checked):
    if checked == "''":
        pass
    else:
        checked = checked.split(', ');

        for check in checked:
            path = "//label[contains(.,'{}')]/input".format(check)
            context.browser.find_by_xpath(path).click()

@then('I see "{count}" members in my list')
def impl(context, count):
    members = context.browser.find_by_css('.user-card')
    assert len(members) == int(count)


# Unique to Scenario: View full profile
@when('I click on "View Full Profile" on a member card')
def impl(context):
    # Wait for the other users to load (check for the report abuse link)
    if context.browser.is_element_present_by_css('a.report-abuse', wait_time=20):
        context.browser.find_link_by_text('View Full Profile').last.click()

@then('I see more information about the member')
def impl(context):
    pass

@then('"View Full Profile" turns into "Collapse"')
def impl(context):
    pass


