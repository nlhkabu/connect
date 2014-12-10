Feature: Invite Users

    Scenario: Moderator views page
        Given a logged in moderator
        When the moderator views the 'invite users' page
        Then we see a form for inviting users

    Scenario: Moderator invites a new user
        Given a logged in moderator
        When the moderator provides a first name, last name and email
        Then the invited user's details appears in a table below

    Scenario: No first name provided
        Given a logged in moderator
        When the moderator tries to invite a new user
        But does not provide a first name
        Then a validation error appears

    Scenario: No last name provided
        Given a logged in moderator
        When the moderator tries to invite a new user
        But does not provide a last name
        Then a validation error appears

    Scenario: No email provided
        Given a logged in moderator
        When the moderator tries to invite a new user
        But does not provide an email address
        Then a validation error appears

    Scenario: Invalid email address
        Given a logged in moderator
        When the moderator tries to invite a new user
        But does the email address is invalid
        Then a validation error appears

    Scenario: Email address already registered
        Given a logged in moderator
        When the moderator tries to invite a new user
        But the email address is already registered to another user
        Then a validation error appears

    Scenario: Moderator reinvites user
        Given a logged in moderator
        And an invited user
        When the moderator reinvites the user
        Then we see a success message

    Scenario: Moderator tries to reinvite user without email address
        Given a logged in moderator
        And an invited user
        When the moderator reinvites the user
        But submits the form without an email
        Then we see a validation message

    Scenario: Moderator revokes invitation
        Given a logged in moderator
        And an invited user
        When the moderator revokes the invitation
        Then we see a popup confirmation modal
        And the invited user is removed from the table
