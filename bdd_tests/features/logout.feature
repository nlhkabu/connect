Feature: Logout

    Scenario: User logs out
        Given I am an authenticated user
        When I clicks on the logout link
        Then I am no longer authenticated
        And I am redirected to the login page
