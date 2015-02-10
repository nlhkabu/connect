Feature: Revoke Invitation
    As a moderator
    I want to revoke an invitation I have previously made
    So that I can fix my mistakes

    Background: The logged in moderator has invited a user
        Given there is a moderator in the database
        And I am logged in as that moderator
        And I have invited a new member to the application

    Scenario: Launch modal
        Given I am "a logged in moderator"
        When I visit the "invite user" page
        And I click on "Revoke Invitation"
        Then the "Revoke Invitation" modal pops up

    Scenario: Close modal
        Given I am "a logged in moderator"
        And I have launched the "revoke invitation" modal
        When I click on the close button
        Then the modal closes

    Scenario: Moderator does not confirm revocation
        Given I am "a logged in moderator"
        And I have launched the "revoke invitation" modal
        When I do not check the confirmation box
        And I submit the modal form
        Then I see "This field is required."

    Scenario: Moderator confirms revocation
        Given I am "a logged in moderator"
        And I have launched the "revoke invitation" modal
        When I check the confirmation box
        And I submit the modal form
        Then I see "Invited User has been uninvited from example.com."
        And the invited user has been removed from my pending invitations list
