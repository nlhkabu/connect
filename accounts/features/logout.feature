@login_std_user
Feature: Logout

    Scenario: User logs out
        Given I am a logged in user
        When I click on the logout link
        Then I am no longer authenticated
        And I am redirected to the login page
