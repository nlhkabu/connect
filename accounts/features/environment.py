# Used with Behave to define code to run before and after certain events during BDD testing.

from behave import *
from splinter.browser import Browser

from accounts.factories import UserFactory, RoleFactory, SkillFactory
from connect_config.factories import SiteConfigFactory

def before_all(context):
    context.browser = Browser()
    context.server_url = 'http://localhost:8000/' #TODO: make this dynamic using site.url

    # Now I need to setup a local database and launch a local server....

    # Setup Users:

    #~|   first name  |   last name     |    email                      |   pass    |   is_active   |   is_closed   |   auth_token  |
    #~|   Active      |   User1         |    active.user1@test.test     |   pass    |   true        |   false       |   123456      |
    #~|   Inactive    |   User2         |    inactive.user@test.test    |   pass    |   false       |   false       |   7891011     |
    #~|   Closed      |   User3         |    closed.user3@test.test     |   pass    |   false       |   true        |   4563543     |


    # Setup Roles:
    #~|   role    |
    #~|   role1   |
    #~|   role2   |


    # Setup Skills
    #~|   skill   |
    #~|   skill1  |
    #~|   skill2  |

def after_all(context):
    context.browser.quit()
    context.browser = None



