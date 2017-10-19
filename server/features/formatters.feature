Feature: Formatters
    # This feature is just to ensure that the formatters endpoint work.
    @auth
    Scenario: List preview formatters
        When we get "formatters?criteria=can_preview"
        Then we get OK response

    @auth
    Scenario: List export formatters
        When we get "formatters?criteria=can_export"
        Then we get OK response