Feature: Moderation Logs

    Background: The database contains a number of logs
        Given that there is an invitation log from today
        And there is a reinvitation log from yesterday
        And there is an invitation log fom three days ago
        And there is a user ban log from a month ago

    Scenario: User views logs page
        Given I am an authenticated moderator
        When I visit the logs page
        Then I see a table with logs in it

    Scenario: User filters logs by type
        Given I am an authenticated moderator
        When I filter the logs by type
        Then I can only see that type of log in the table

    Scenario: User filters logs by date
        Given I am an authenticated moderator
        When I filter the logs by date range
        Then I can only see logs that were logged during that date range

    Scenario: User filters logs by type and date
        Given I am an authenticated moderator
        When I filter the logs by type
        And I filter the logs by date range
        Then I can only see logs that are of that type and logged during that date range
