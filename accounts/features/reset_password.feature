Feature: Reset Password

    Background: There is a registered user in the database with the email 'my.email@test.test'

    Scenario: User submits invalid data to reset password form
        Given I am a registered user
        When I input <email>
        Then I see <error>

        Examples:
            |   email           |   error                                  |
            |   ''              |   This field is required.                |
            |   invalidemail    |   Please enter a valid email address.    |

    Scenario: User requests password reset
        """
        Note that passing in an unregistered email should still result in a
        redirect - as we don't want to expose user information.
        """
        Given I am a registered user
        When I input <email>
        Then I am taken to a confirmation page
        And I see 'Please check your email'

        Examples:
            |   email                           |
            |   my.email@test.test              |
            |   unregistered.email@test.test    |

