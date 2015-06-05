Feature: Invite User
    As a moderator
    I want to invite a new user
    So that they can join the community

    Background: There are two users in the database, one of whom is a moderator
        Given there is a standard user in the database
        And there is a moderator in the database
        And I am logged in as that moderator

    Scenario Outline: Moderator submits invalid data to the invite user form
        Given I am "a logged in moderator"
        When I visit the "invite user" page
        And I enter "<full name>" into the "full name" field
        And I enter "<email>" into the "email" field
        And I submit the form
        Then I see "<error>"

        Examples:
            |   full name   |    email                      |   error                                                               |
            |   ""          |    new.user@test.test         |   Please enter a full name.                                           |
            |   First Last  |    ""                         |   Please enter an email address.                                      |
            |   First Last  |    invalidemail               |   Please enter a valid email address.                                 |
            |   First Last  |    standard.user@test.test    |   Sorry, this email address is already registered to another user.    |

    Scenario: Moderator invites new user
        Given I am "a logged in moderator"
        And I invite a new user, with the name "First Last"
        Then I see "First Last has been invited to example.com."
        And I see that the user has been added to my list of invitations pending activation
