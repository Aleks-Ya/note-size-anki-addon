#noinspection CucumberUndefinedStep
Feature: Size of current note in Browser

  @S0601 @smoke @browser @editor
  Scenario: Show size of current note in Browser

    Given I opened Browser
    And I selected Note
    Then "Note Size Button" is displayed

    When I clicked "Note Size Button"
    Then "Details Dialog" is displayed

    When I clicked "Note Size Button" again
    Then Existing "Details Dialog" has closed
    Then New "Details Dialog" is displayed

    When I clicked Close button
    Then "Details Dialog" has closed