#noinspection CucumberUndefinedStep
Feature: Performance of size calculation

  @smoke @browser @editor
  Scenario: Show size of huge collection

    Given I generated huge collection
    And I opened Anki
    Then "Initialization Dialog" finished quickly
