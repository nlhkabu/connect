Feature: View Dashboard
    As a registered user
    I want to search for and view other members information
    So that I find interesting people to connect with

    Background: There are many members with a variety of skills and roles
        Given there is a standard, active user in the database
        And I am logged in as that standard user
        And the following users exist:
            |    email              |   skills          |   roles           |
            |    email1@test.test   |   skill1, skill2  |   ''              |
            |    email2@test.test   |   ''              |   role1, role2    |
            |    email3@test.test   |   skill1          |   role1           |
            |    email4@test.test   |   skill2          |   ''              |
            |    email5@test.test   |   skill1, skill2  |   role2           |
            |    email6@test.test   |   skill1, skill2  |   role1, role2    |
            |    email7@test.test   |   skill2          |   role1           |

    Scenario: User views dashboard
        Given I am "a logged in user"
        When I visit the "dashboard" page
        Then I see the application name in the banner
        And I see a list of members, including myself

    Scenario Outline: Filter members
        Given I am "a logged in user"
        When I visit the "dashboard" page
        And I filter members by "<skills>"
        And I filter members by "<roles>"
        And I submit the form
        Then I see "<count>" members in my list

        Examples:
            |   skills          |   roles           |   count   |
            |   skill1          |   ''              |   4       |
            |   skill1, skill2  |   ''              |   6       |
            |   skill1          |   role1           |   2       |
            |   ''              |   role1           |   4       |
            |   ''              |   role1, role2    |   5       |
            |   skill1, skill2  |   role1, role2    |   4       |
            |   ''              |   role3           |   0       |

    Scenario: View full profile
        Given I am "a logged in user"
        When I visit the "dashboard" page
        And I click on "View Full Profile" on a member card
        Then the member card expands
        And "View Full Profile" turns into "Collapse"

    Scenario: Report Abuse
        Given I am "a logged in user"
        When I visit the "dashboard" page
        And I click on "Report Abuse" on another member's card
        Then I am taken to a new page to report that member

    Scenario: Many users prompt pagination
        Given I am "a logged in user"
        And pagination is set to start at 3 users
        When I visit the "dashboard" page
        Then I see that the list of members is paginated
