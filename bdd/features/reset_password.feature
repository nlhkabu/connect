Feature: Reset Password
    As a registered user
    I want to reset my password
    So that I can access my account when I've forgotten my password

    Background: There is one user in the database
        Given there is a standard user in the database
        And I am logged in as that standard user

    Scenario Outline: User submits data to reset password form
        """
        Note that passing in an unregistered email should still result in a
        redirect - as we don't want to expose user information.
        """
        Given I am "a logged out user"
        When I visit the "reset password" page
        And I enter "<email>" into the "email" field
        And I submit the form
        Then I see "<message>"

        Examples:
            |   email                   |   message                             |
            |   ""                      |   This field is required.             |
            |   invalidemail            |   Please enter a valid email address. |
            |   standard.user@test.test |   Please check your email             |
            |   not.a.user@test.test    |   Please check your email             |

