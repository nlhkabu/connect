Feature: Reset Password

    Scenario: User requests reset email
        Given I am a registered user
        When I request an email to reset my password
        Then I am taken to a confirmation page

    Scenario: Invalid email
        Given I am a registered user
        When I request an email to reset my password
        But I enter my email incorrectly
        Then I am taken to a confirmation page

    Scenario: Unregistered email
        Given I am an unregistered user
        When I request an email to reset my password
        Then I am taken to a confirmation page (but an email is not sent)
