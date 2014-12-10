Feature: Dashboard

    Background: The database is set up and there are many registered users
        Given that the site details have been configured
        And there are skills in the database
        And there are roles in the database
        And there are 10+ active users
        And each user has some biographical information associated with it

    Scenario: User views page
        Given I am an authenticated user
        When I visit the dashboard
        Then I see the application name, logo and tagline
        And I see a list of all active members, with information on each one

    Scenario: Many users prompt pagination
        Given I am an authenticated user
        When I visit the dashboard
        Then I see that the list of members is paginated

    Scenario: Filter member by skill
        Given I am authenticated user
        When I filter the list of members by a single skill
        Then I see only the members who have that skill

    Scenario: Filter member by multiple skills
        Given I am an authenticated user
        When I filter the list of members by multiple skills
        Then I see the members who either skill

    Scenario: Filter member by role
        Given I am an authenticated user
        When I filter the list of members by a single role
        Then I see the members who have that role

    Scenario: Filter member by multiple roles
        Given I am an authenticated user
        When I filter the list of members by multiple roles
        Then I see the members who have either role

    Scenario: Filter member by skill and role
        Given I am an authenticated user
        When I filter the list of members by a skill and a role
        Then I see only the members who have the that skill and that role

    Scenario: No results
        Given I am an authenticated user
        When I filter the list of members by too many parameters
        Then I see a card saying 'no results'

    Scenario: View full profile
        Given I am an authenticated user
        When I click on 'View Full Profile' on a member card
        Then I see more information about the member
        And 'View Full Profile' turns into 'Collapse'

    Scenario: Report Abuse
        Given I am an authenticated user
        When I click on 'Report Abuse' on another member's card
        Then I am taken to a new page to report that member
