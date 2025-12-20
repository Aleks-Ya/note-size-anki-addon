#noinspection CucumberUndefinedStep
Feature: Dark Theme

  @S0901 @smoke @browser @editor
  Scenario: UI elements are visible in Dark Theme

    Given "Light Theme" is active
    And Deck Browser is opened

    When I clicked Tools - Preferences
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

  @S0902 @browser @editor @add
  Scenario: Switch opened dialogs to Dark Theme

    Given "Light Theme" is active
    And Deck Browser is opened

    And I opened "Add New Note Window"
    And I clicked "Size Button"

    And I opened Browser
    And I clicked "Notes Size Button"
    And I clicked "Note Size Button"

    When I switch to "Deck Browser"
    And I clicked Tools - Preferences
    And I clicked "Appearance" tab
    And I selected "Dark Theme"
    Then Anki switched to "Dark Theme"
    Then "Note Size" dialog in "Add New Note Window" switched to "Dark Theme"
    Then "Note Size" dialog in Browser switched to "Dark Theme"
    Then "Notes Size" dialog in Browser switched to "Dark Theme"

    When I switch to "Deck Browser"
    And I clicked Tools - Preferences
    And I clicked "Appearance" tab
    And I selected "Light Theme"
    Then Anki switched to "Light Theme"
    Then "Note Size" dialog in "Add New Note Window" switched to "Light Theme"
    Then "Note Size" dialog in Browser switched to "Light Theme"
    Then "Notes Size" dialog in Browser switched to "Light Theme"
