Feature: View Dashboard

    Background: The database is set up and there are many registered users
        Given that the site details have been configured
        And the following skills are in the database:
            |   skill   |
            |   skill1  |
            |   skill2  |

        And the following roles are in the database:
            |   role    |
            |   role1   |
            |   role2   |
            |   role3   |

        And the following users are in the database:
            |   first name  |   last name   |    email              |   skills          |   roles           |
            |   first       |   last        |    email1@test.test   |   skill1, skill2  |   ''              |
            |   first       |   last        |    email2@test.test   |   ''              |   role1, role2    |
            |   first       |   last        |    email3@test.test   |   skill1          |   role1           |
            |   first       |   last        |    email4@test.test   |   skill2          |   ''              |
            |   first       |   last        |    email5@test.test   |   skill1, skill2  |   role2           |
            |   first       |   last        |    email6@test.test   |   skill1, skill2  |   role1, role2    |
            |   first       |   last        |    email7@test.test   |   skill2          |   role1           |

    Scenario: User views page
        Given I am an authenticated user
        When I visit the dashboard
        Then I see the application name, logo and tagline
        And I see a list of all active members, with information on each one

    Scenario Outline: Filter members
        Given I am an authenticated user
        And I filter members by <skills>
        And I filter members by <roles>
        And I submit the form
        The I see <count> members in my list

        Examples:
            |   skills          |   roles           |   count   |
            |   skill1          |   ''              |   4       |
            |   skill1, skill2  |   ''              |   6       |
            |   skill1          |   role1           |   2       |
            |   ''              |   role1           |   4       |
            |   ''              |   role1, role2    |   5       |
            |   skill1, skill2  |   role1, role2    |   4       |

    Scenario: No results
        Given I am an authenticated user
        When I filter the list of members by 'role 3'
        Then I see 'There are no users matching your selected search.'

    Scenario: View full profile
        Given I am an authenticated user
        When I click on 'View Full Profile' on a member card
        Then their card expands
        And I see more information about them
        And 'View Full Profile' turns into 'Collapse'

    Scenario: Report Abuse
        Given I am an authenticated user
        When I click on 'Report Abuse' on another member's card
        Then I am taken to a new page to report that member

    Scenario: Many users prompt pagination
        Given I am an authenticated user
        And there are over 20 users in the database
        When I visit the dashboard
        Then I see that the list of members is paginated
