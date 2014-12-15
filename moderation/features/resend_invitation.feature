Feature: Resend Invitation

    Background: The logged in moderator has invited a user
        Given that I am a logged in moderator
        And the following user is in my 'users pending activation' list:
            |   first name  |   last name   |   email               |
            |   New         |   User        |   new.user@test.test  |

    Scenario: Clicking on 'resend invitation' launches modal
        Given I am a logged in moderator
        When I click on 'resend invitation'
        Then a modal containng a resend invitation form pops up
        And the user's email is prepopulated in the form

    Scenario: Close modal
        Given I am a logged in moderator
        And I have launched the 'resend invitation' modal
        When I click on the close button
        Then the modal closes

    Scenario Outline: Moderator submits invalid data to the resend invitation form
        Given I am a logged in moderator
        And 'taken.email@test.test' is registered to another user
        And I have launched the 'resend invitation' modal
        When I input <email>
        And I submit the form
        Then I see <error>

        Examples:
            |   email                   |   error                                                               |
            |   ''                      |   This field is required.                                             |
            |   notanemail              |   Please enter a valid email.                                         |
            |   taken.email@test.test   |   Sorry, this email address is already registered to another user.    |

    Scenario: Moderator resends invitation
        Given I am a logged in moderator
        And I have launched the 'resend invitation' modal
        When I input 'new.user@test.test'
        And I submit the form
        Then I see 'New User has been reinvited to Connect.'
