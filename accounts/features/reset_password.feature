Feature: Reset Password

    Scenario Outline: User submits invalid data to reset password form
        Given I am a logged out user
        When I visit the reset password page
        And I input <email> into the email field
        And I submit the form
        Then I see <error>

        Examples:
            |   email           |   error                           |
            |   ""              |   "This field is required."       |
            |   "invalidemail"  |   "Enter a valid email address."  |

    Scenario Outline: User requests password reset
        """
        Note that passing in an unregistered email should still result in a
        redirect - as we don't want to expose user information.
        """
        Given I am a logged out user
        When I visit the reset password page
        And I input <email> into the email field
        And I submit the form
        Then I am taken to a confirmation page that says "Please check your email"

        Examples:
            |   email                       |
            |   "active.user@test.test"     |
            |   "not.a.user@test.test"      |

