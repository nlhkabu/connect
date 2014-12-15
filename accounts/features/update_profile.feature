Feature: Update Profile

    Background: The database is configured and contains skills and roles
        Given that the site details have been configured
        And the following skills are in the database:
            |   role    |
            |   role1   |
            |   role2   |

        And the following roles are in the database:
            |   skill   |
            |   skill1  |
            |   skill2  |

        And the profile form includes two link forms
        And the profile form includes two skill forms

    Scenario: User views page
        Given I am an authenticated user
        When I visit the profile page
        Then I see the profile settings form
        And the form is prepopulated with my data

    Scenario Outline: User submits invalid data to update profile form
        Given I am an authenticated user
        When I input <first name>
        And I input <last name>
        And I input <link 1 anchor>
        And I input <link 1 url>
        And I input <link 2 anchor>
        And I input <link 2 url>
        And I select <skill 1 name>
        And I select <skill 1 proficiency>
        And I select <skill 2 name>
        And I select <skill 2 proficiency>
        And I submit the form
        Then I see <error>

        Examples:
            |   first name  |   last name   |   link 1 anchor   |   link 1 url          |   link 2 anchor   |   link 2 url          |   skill 1 name    |   skill 1 proficiency |   skill 2 name    |   skill 2 proficiency |   error                                       |
            |   ''          |   Last        |   My link         |   http://myurl.com    |   My link2        |   http://myurl2.com   |   skill1          |   BEGINNER            |   skill2          |   EXPERT              |   This field is required.                     |
            |   First       |   ''          |   My link         |   http://myurl.com    |   My link2        |   http://myurl2.com   |   skill1          |   BEGINNER            |   skill2          |   EXPERT              |   This field is required.                     |
            |   First       |   Last        |   ''              |   http://myurl.com    |   My link2        |   http://myurl2.com   |   skill1          |   BEGINNER            |   skill2          |   EXPERT              |   All links must have an anchor.              |
            |   First       |   Last        |   My link1        |   ''                  |   My link2        |   http://myurl2.com   |   skill1          |   BEGINNER            |   skill2          |   EXPERT              |   All links must have a url.                  |
            |   First       |   Last        |   My link1        |   http://myurl.com    |   My link1        |   http://myurl2.com   |   skill1          |   BEGINNER            |   skill2          |   EXPERT              |   Links must have unique anchors and URLs.    |
            |   First       |   Last        |   My link1        |   http://myurl.com    |   My link2        |   http://myurl.com    |   skill1          |   BEGINNER            |   skill2          |   EXPERT              |   Links must have unique anchors and URLs.    |
            |   First       |   Last        |   My link1        |   http://myurl.com    |   My link2        |   http://myurl.com    |   skill1          |   BEGINNER            |   skill2          |   EXPERT              |   Links must have unique anchors and URLs.    |
            |   First       |   Last        |   My link         |   http://myurl.com    |   My link2        |   http://myurl2.com   |   ''              |   BEGINNER            |   skill2          |   EXPERT              |   All skills must have a skill name.          |
            |   First       |   Last        |   My link         |   http://myurl.com    |   My link2        |   http://myurl2.com   |   skill1          |   ''                  |   skill2          |   EXPERT              |   All skills must have a proficiency.         |
            |   First       |   Last        |   My link         |   http://myurl.com    |   My link2        |   http://myurl2.com   |   skill1          |   BEGINNER            |   skill1          |   EXPERT              |   Each skill can only be entered once.        |

    Scenario: Biography field expands
        Given I am an authenticated user
        When I add more than three lines to the biography field
        Then the field 'grows' to accommodate the text

    Scenario: Remove a form from the skills list
        Given I am an authenticated user
        When I click on 'remove' next to a skill form
        Then this form is removed from the list

    Scenario: Add another form to the skills list
        Given I am an authenticated user
        When I click on 'add skill'
        Then another skill formset is added to the bottom of the form

    Scenario: Remove a form from the links list
        Given I am an authenticated user
        When I click on 'remove' next to a link form
        Then this form is removed from the list

    Scenario: Add another form to the links list
        Given I am an authenticated user
        When I click on 'add link'
        Then another link formset is added to the bottom of the form

    Scenario: Update user's profile
        Given I am an authenticated user
        When I input 'First'
        And I input 'Last'
        And I input 'my bio'
        And I input 'My Anchor 1'
        And I input 'http://myurl1.com'
        And I input 'My Anchor 2'
        And I input 'http://myurl2.com'
        And I check 'role1'
        And I select 'skill1'
        And I select 'BEGINNER'
        And I select 'skill2'
        And I select 'INTERMEDIATE'
        And I submit the form
        Then I see 'Your profile has been updated'
