#noinspection CucumberUndefinedStep
Feature: Switch profile

  @S1001 @smoke @browser @editor
  Scenario: Switch to the same profile

    Given "User 1" profile is opened
    When I click File - Switch Profile
    Then "Profiles" dialog is opened
    When I open "User 1" profile
    Then Deck Browser is opened
    Then Collection Size is displayed in Deck Browser
