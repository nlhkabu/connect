Feature: Review Abuse Reports

    Background: The database is set up with several abuse reports
        Given there are two standard users
        And a moderator
        And the standard users have logged abuse reports against each other

    Scenario: Visit abuse report page
        Given I am an authenticated moderator
        When I visit the abuse reports page
        Then I see a list of abuse reports
        But I cannot see reports relating to myself

    Scenario: Address Abuse Report
        Given I am an authenticated moderator
        When I moderate an abuse report
        Then the report is removed from the list

    Scenario: No comment
        Given I am an authenticated moderator
        When I moderate an abuse report
        But forget to put in a comment
        Then I see an error message
