Feature: View Moderation Logs

    Background: The database contains a number of logs
        Given the following logs exist:
            |   log type        |   log datetime    |
            |   invitation      |   today           |
            |   reinvitation    |   yesterday       |
            |   invitation      |   yesterday       |
            |   invitation      |   three days ago  |
            |   ban user        |   one month ago   |
            |   warn user       |   two months ago  |

    Scenario: User views logs page
        Given I am an authenticated moderator
        When I visit the logs page
        Then I see a table with four logs in it

    Scenario: Filter logs by type and period
        Given I am an authenticated moderator
        When I select <type>
        And I select <period>
        And I submit the form
        Then I see <count> logs

        Examples:
            |   type            |   period      |   count   |
            |   invitation      |   all         |   3       |
            |   invitation      |   today       |   1       |
            |   all             |   yesterday   |   2       |
            |   reinvitation    |   yesterday   |   1       |
            |   all             |   this week   |   3       |

    Scenario: Date fields appear when 'custom' period is selected
        Given I am an authenticated moderator
        When I select 'custom' period
        Then the 'start date' field appears
        And the 'end date' field appears

    Scenario: Filter logs by custom date range
        Given I am an authenticated moderator
        And I have selected 'custom'
        When I input a date from a month ago in the 'start date' field
        And I input todays date in the 'end date' field
        And I submit the form
        Then I see one log
