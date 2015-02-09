Feature: Update Email
    As a registered user
    I want to change my email address
    So that I can keep my settings up to date

    Background: There are two users in the database
        Given there is an invited, but not yet active user in the database
        And there is a standard user in the database
        And I am logged in as that standard user

    Scenario: User views page
        Given I am "a logged in user"
        When I visit the "update email" page
        Then I see the update email form, prepopulated with my email

    Scenario Outline: User submits data to the update email form
        Given I am "a logged in user"
        When I visit the "update email" page
        And I enter "<email>" into the "email" field
        And I enter "<password>" into the "password" field
        And I submit the form
        Then I see "<message>"

        Examples:
            |   email                   |   password    |   message                                                             |
            |   ""                      |   pass        |   This field is required.                                             |
            |   invalidemail            |   pass        |   Please enter a valid email address.                                 |
            |   inactive.user@test.test |   pass        |   Sorry, this email address is already registered to another user.    |
            |   a.new.email@test.test   |   ""          |   This field is required.                                             |
            |   a.new.email@test.test   |   wrongpass   |   Incorrect password. Please try again.                               |
            |   a.new.email@test.test   |   pass        |   Your example.com email has been updated.                            |

