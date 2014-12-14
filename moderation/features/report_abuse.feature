Feature: Report Abuse

    Background: There are at least two active users in the database
        Given the following users exist:
            |   first name  |   last name   |   email               |
            |   User        |   One         |   user.one@test.test  |
            |   User        |   Two         |   user.two@test.test  |

    Scenario: User reports another user
        Given I am an authenticated user
        When I click on the link to report another user
        And I fill out the comments
        And I submit the form
        Then I am redirected to a new page
        And I see 'Your Abuse Report has been logged'

    Scenario: User attempts to report another user without comments
        Given I am an authenticated user
        When I click on the link to report another user
        But I do not fill out the comments
        And I submit the form
        Then I see 'This field is required.'
