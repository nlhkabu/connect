Feature: View Moderation Logs

    Background: The database contains a number of logs
        Given there is a moderator in the database
        And I am logged in as that moderator
        And the following logs exist:
            |   log type        |   log datetime    |
            |   invitation      |   today           |
            |   reinvitation    |   yesterday       |
            |   invitation      |   yesterday       |
            |   invitation      |   three days ago  |
            |   ban user        |   one month ago   |
            |   warn user       |   two months ago  |

    Scenario: User views logs page
        Given I am "a logged in moderator"
        When I visit the "logs" page
        Then I see a table with six logs in it

    Scenario Outline: Filter logs by type and period
        Given I am "a logged in moderator"
        When I visit the "logs" page
        And I select "<type>" from the "msg_type" dropdown
        And I select "<period>" from the "period" dropdown
        And I submit the form
        Then I see "<count>" logs

        Examples:
            |   type                    |   period                  |   count   |
            |   Invitation              |   All                     |   3       |
            |   Invitation              |   Today                   |   1       |
            |   All                     |   Yesterday               |   2       |
            |   Invitation Resent       |   Yesterday               |   1       |
            |   All                     |   This Week (Last 7 days) |   4       |
            |   Application Rejected    |   Today                   |   0       |

    Scenario: Date fields appear when 'custom' period is selected
        Given I am "a logged in moderator"
        When I visit the "logs" page
        And I select "Custom Date Range" from the "period" dropdown
        Then the "start date" field appears
        And the "end date" field appears

    Scenario: Filter logs by custom date range
        Given I am "a logged in moderator"
        When I visit the "logs" page
        And I select "Custom Date Range" from the "period" dropdown
        And I input a date from a month ago in the start date field
        And I input todays date in the end date field
        And I submit the form
        Then I see "5" logs

    Scenario: Attempt to filter logs by custom date range, without specifying a date
        Given I am "a logged in moderator"
        When I visit the "logs" page
        And I select "Custom Date Range" from the "period" dropdown
        But I do not select a date
        And I submit the form
        Then I see "To filter by date, please provide a start and end date"
