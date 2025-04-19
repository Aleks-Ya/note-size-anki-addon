#noinspection CucumberUndefinedStep
Feature: Size of current note in Add Window

  @smoke @add
  Scenario: Show size of current note in Add Window

    Given I opened Browser
    And I selected Note
    Then "Note Size Button" is displayed

    When I clicked "Note Size Button"
    Then "Detail Dialog" is displayed
