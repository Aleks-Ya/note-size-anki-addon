#noinspection CucumberUndefinedStep
Feature: Performance of size calculation

  @S1301 @smoke @browser @editor
  Scenario: Show size of huge collection

    Given I generated huge collection (200k notes)
    And I opened Anki
    Then "Initialization Dialog" finished quickly

    When I open Browser
    And I search for "deck:*"
    And I clicked "Notes Size Button"
    Then "Progress Dialog" is displayed
    Then "Details Dialog" is displayed
