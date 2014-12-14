Feature: Revoke Invitation

    Background: The logged in moderator has invited a user
        Given that I am a logged in moderator
        And the following user is in my 'users pending activation' list:
            |   first name  |   last name   |   email               |
            |   New         |   User        |   new.user@test.test  |

    Scenario: Clicking on 'revoke invitation' launches modal
        Given I am a logged in moderator
        When I click on 'revoke invitation'
        Then a modal containng a revoke invitation form pops up

    Scenario: Close modal
        Given I am a logged in moderator
        And I have launched the 'revpke invitation' modal
        When I click on the close button
        Then the modal closes

    Scenario: Moderator does not confirm revocation
        Given I am a logged in moderator
        And I have launched the 'revoke invitation' modal
        But I do not tick the confirmation box
        And I submit the form
        Then I see 'Please confirm you with to revoke your invitation to New User'

    Scenario: Moderator does not confirm revocation
        Given I am a logged in moderator
        And I have launched the 'revoke invitation' modal
        And I tick the confirmation box
        And I submit the form
        Then I see 'Your invitation to New User has been revoked.'

