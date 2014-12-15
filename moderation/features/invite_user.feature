Feature: Invite User

    Scenario: Moderator views page
        Given I am a logged in moderator
        When I view the 'invite users' page
        Then I see a form for inviting users

    Scenario Outline: Moderator submits invalid data to the invite user form
        Given I am a logged in moderator
        And 'taken.email@test.test' is already registered with another user
        And I input <first name>
        And I input <last name>
        And I input <email>
        And I submit the form
        Then I see <error>

        Examples:
            |   first name  |   last name   |    email                      |   error                                                               |
            |   ''          |   last        |    'new.email@test.test'      |   This field is required.                                             |
            |   first       |   ''          |    'new.email@test.test'      |   This field is required.                                             |
            |   first       |   last        |    ''                         |   This field is required.                                             |
            |   first       |   last        |    'invalidemail'             |   Please enter a valid email address.                                 |
            |   first       |   last        |    'taken.email@test.test'    |   Sorry, this email address is already registered to another user.    |

    Scenario: Moderator submits valid data to the invite user form
        Given I am a logged in moderator
        When I input 'first'
        And I input 'last'
        And I input 'unique.email@test.test'
        And I submit the form
        Then I see 'first last has been invited to Connect'.
        And I see that 'first last' has been added to my list of invitations pending activation
