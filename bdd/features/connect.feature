Feature: Connect With Another User
    As a user
    I want to connect with another user
    So that I can collaborate with them

    Background: There are two users in the database
        Given there are two standard users in the database

    Scenario: First user clicks on the 2nd user's connect button
        Given I am logged in as the first standard user
        When I click on the connect button of the second user
        Then I will be redirected to the connect page
