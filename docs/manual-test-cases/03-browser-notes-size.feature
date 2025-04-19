#noinspection CucumberUndefinedStep
Feature: Size of notes found in Browser

  @smoke @browser
  Scenario: Show size of notes found in Browser

    Given I opened Browser
    And I searched for notes
    Then "Notes Size Button" is displayed

    When I clicked "Notes Size Button"
    Then "Detail Dialog" is displayed
