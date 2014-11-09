Feature: Dashboard

    Scenario: Authenticated user views page
        Given an authenticated user
        When we visit the dashboard
        Then we see the application name, logo and tagline
        And we see a list of all active members, with information on each one

    Scenario: Unauthenticated user views page
        Given an unauthenticated user
        When we visit the dashboard
        Then we are redirected to the login page

    Scenario: Filter member by skill
        Given an authenticated user
        When we click on 'django'
        And we click 'refine results'
        Then we see only the members who have the skill 'django'

    Scenario: Filter member by role
        Given an authenticated user
        When we click on 'mentor'
        And we click 'refine results'
        Then we see only the members who have the role 'mentor'

    Scenario: Filter member by skill and role
        Given an authenticated user
        When we click on 'django'
        And we click on 'mentor'
        And we click 'refine results'
        Then we see only the members who have the skill 'django' and the role 'mentor'

    Scenario: View full profile
        Given a member card
        When we click on 'View Full Profile'
        Then we see more information about the member
        And 'View Full Profile' turns into 'Collapse'

    Scenario: Report Abuse
        Given a member card
        When we click on 'Report Abuse' on that member card
        Then we are taken to a new page to report that member

