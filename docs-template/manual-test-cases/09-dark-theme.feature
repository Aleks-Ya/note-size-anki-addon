#noinspection CucumberUndefinedStep
Feature: Dark Theme

  @smoke @browser @editor
  Scenario: Switch to Dark Theme

    Given "Light Theme" is active
    And I clicked Tools - Preferences
    And I clicked "Appearance" tab
    And I selected "Dark Theme"
    Then Anki switched to "Dark Theme"
    Then "Collection Size" in Deck Browser is visible

    When I clicked "Configuration" icon
    Then "Configuration" dialog is visible

    When I opened Browser
    Then "Size Button" is visible on small notes
    Then "Size Button" is visible on medium notes
    Then "Size Button" is visible on big notes

    When I opened "Details Dialog"
    Then "Details Dialog" is visible
