#noinspection CucumberUndefinedStep
Feature: Size of current note in Browser

  @smoke @browser @editor
  Scenario: Show size of current note in Browser

    Given I opened Browser
    And I selected Note
    Then "Note Size Button" is displayed

    When I clicked "Note Size Button"
    Then "Detail Dialog" is displayed
