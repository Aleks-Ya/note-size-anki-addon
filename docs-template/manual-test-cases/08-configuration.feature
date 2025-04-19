#noinspection CucumberUndefinedStep
Feature: Configuration dialog

  @smoke @deck_browser
  Scenario: Hide "Collection Size" from Deck Browser

    Given I opened "Configuration Dialog"
    When I click "Deck Browser" tab
    When I unmark "Show collection size in Deck Browser"
    When I click "OK" button
    Then "Collection Size" is not displayed in Deck Browser

    When I opened "Configuration Dialog"
    When I click "Deck Browser" tab
    When I mark "Show collection size in Deck Browser"
    When I click "OK" button
    Then "Collection Size" is displayed in Deck Browser

  @smoke @browser
  Scenario: Hide "Collection Size" from Deck Browser

    Given I opened "Configuration Dialog"
    When I click "Browser" tab
    When I unmark "Show size of notes found in Browser"
    When I click "OK" button
    Then "Notes Size Button" is not displayed in Browser

    When I opened "Configuration Dialog"
    When I click "Browser" tab
    When I unmark "Show size of notes found in Browser"
    When I click "OK" button
    Then "Notes Size Button" is displayed in Browser

  @smoke @browser @editor
  Scenario: Hide "Size Button" from Editor
    Given I opened "Configuration Dialog"
    When I click "Editor" tab
    When I unmark "Show note size in Editor"
    When I click "OK" button
    Then "Size Button" is not displayed in Browser
    Then "Size Button" is not displayed in Add New Note Window

    When I opened "Configuration Dialog"
    When I click "Editor" tab
    When I mark "Show note size in Editor"
    When I click "OK" button
    Then "Size Button" is displayed in Browser
    Then "Size Button" is displayed in Add New Note Window

  @smoke @browser @editor
  Scenario: Disable colors of "Size Button"
    Given I opened "Configuration Dialog"
    When I click "Editor" tab
    When I unmark "Enable colors"
    When I click "OK" button
    Then "Size Button" has no color in Browser
    Then "Size Button" has no color in Add New Note Window

    When I opened "Configuration Dialog"
    When I click "Editor" tab
    When I mark "Enable colors"
    When I click "OK" button
    Then "Size Button" has color in Browser
    Then "Size Button" has color in Add New Note Window

  @smoke
  Scenario: Refresh cache
    Given I opened "Configuration Dialog"
    When I click "Cache" tab
    When I click "Refresh cache" button
    Then "Progress dialog" has displayed