Feature: Authentication

  Scenario: Valid Login
     Given the login page
      when we put in a valid username and password
      then we are redirected to the dashboard

  Scenario: Invalid email
     Given the login page
      when we put in an invalid email
      then we are told it is invalid

  Scenario: Unregistered email
     Given the login page
      when we put in an unregistered email
      then we are told it is unregistered

  Scenario: Unregistered email
     Given the login page
      when we put in the incorrect password
      then we are told it is incorrect
