Feature: Resend Invitation
    As a moderator
    I want to resend an invitation
    So that I can remind invited users that they have not yet activated their account
    And I can send the invitation to a different email address

    Background: The logged in moderator has invited a user
        Given there is a moderator in the database
        And I am logged in as that moderator
        And I have invited a new member to the application
        And there is a standard user in the database

    Scenario: Clicking on 'resend invitation' launches modal
        Given I am "a logged in moderator"
        When I visit the "invite user" page
        And I click on "Resend Invitation"
        Then the "Resend Invitation" modal pops up
        And the invited user's email is prepopulated in the form

    Scenario: Close modal
        Given I am "a logged in moderator"
        And I have launched the "resend invitation" modal
        When I click on the close button
        Then the modal closes

    Scenario Outline: Moderator submits data to the resend invitation form
        Given I am "a logged in moderator"
        And I have launched the "resend invitation" modal
        When I enter "<email>" into the modal "email" field
        And I submit the modal form
        Then I see "<message>"

        Examples:
            |   email                   |   message                                                             |
            |   ""                      |   Please enter an email address.                                      |
            |   notanemail              |   Please enter a valid email address.                                 |
            |   standard.user@test.test |   Sorry, this email address is already registered to another user.    |
            |   new.email@test.test     |   Invited User has been reinvited to example.com.                     |
