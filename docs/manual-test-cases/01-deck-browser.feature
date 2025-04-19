#noinspection CucumberUndefinedStep
Feature: Collection size in Deck Browser

  @smoke @deck_browser
  Scenario: Show collection size in Deck Browser

    Given I opened Deck Browser
    Then Collection size is displayed
