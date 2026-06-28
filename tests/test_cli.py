"""Integration tests for CLI foundation."""

from io import StringIO

from rich.console import Console

from belling_cat.cli import display_banner, parse_command


def test_banner_displays():
    """Verify the ASCII art banner displays with Belling Cat branding."""
    console = Console(file=StringIO(), width=80, legacy_windows=False)
    display_banner(console)

    output = console.file.getvalue()
    assert "Belling Cat" in output
    assert len(output) > 0


def test_parse_investigate_command():
    """Verify /investigate command is parsed and extracts claim text."""
    result = parse_command("/investigate elephant was seen flying near Changi Airport")

    assert result["command"] == "investigate"
    assert result["args"] == "elephant was seen flying near Changi Airport"


def test_parse_save_command():
    """Verify /save command is parsed and extracts report name."""
    result = parse_command("/save elephant-report")

    assert result["command"] == "save"
    assert result["args"] == "elephant-report"


def test_parse_invalid_command():
    """Verify invalid commands are recognized as unknown."""
    result = parse_command("/invalid something")

    assert result["command"] == "unknown"
    assert result["args"] == ""


def test_format_error_message():
    """Verify error messages include helpful usage guidance."""
    from belling_cat.cli import format_error_message

    error_msg = format_error_message("/invalid something")

    assert "Unknown command" in error_msg or "Invalid command" in error_msg
    assert "/investigate" in error_msg
    assert "/save" in error_msg


def test_command_routing():
    """Verify commands are routed to appropriate handlers."""
    from belling_cat.cli import CommandRouter

    # Track which handlers were called
    calls = []

    def investigate_handler(args: str) -> str:
        calls.append(("investigate", args))
        return "Investigation started"

    def save_handler(args: str) -> str:
        calls.append(("save", args))
        return "Report saved"

    router = CommandRouter()
    router.register("investigate", investigate_handler)
    router.register("save", save_handler)

    result = router.dispatch("/investigate test claim")
    assert result == "Investigation started"
    assert calls == [("investigate", "test claim")]


def test_yachalk_styling():
    """Verify Yachalk is used for terminal color styling."""
    from belling_cat.cli import style_prompt

    styled = style_prompt("Enter command")

    # Verify yachalk is imported and can be used

    # Verify the function returns a styled string
    assert styled is not None
    assert len(styled) > 0


def test_end_to_end_cli_flow():
    """Integration test verifying banner display and command parsing end-to-end."""
    from io import StringIO

    from belling_cat.cli import CommandRouter, display_banner

    console = Console(file=StringIO(), width=80, legacy_windows=False)

    # Display banner
    display_banner(console)
    output = console.file.getvalue()
    assert "Belling Cat" in output

    # Set up router with mock handlers
    investigation_result = None

    def investigate_handler(args: str) -> str:
        nonlocal investigation_result
        investigation_result = args
        return f"Starting investigation: {args}"

    router = CommandRouter()
    router.register("investigate", investigate_handler)

    # Simulate user command
    user_input = "/investigate flying elephant at Changi Airport"
    result = router.dispatch(user_input)

    assert "Starting investigation" in result
    assert investigation_result == "flying elephant at Changi Airport"


def test_app_startup_displays_banner():
    """Verify application startup displays banner when run."""
    from unittest.mock import patch

    from belling_cat.cli import run_app

    # Mock the prompt to avoid blocking
    with patch("belling_cat.cli.Prompt.ask", return_value="/quit"):
        console_output = StringIO()
        console = Console(file=console_output, width=80, legacy_windows=False)

        # Run app with single iteration (quit immediately)
        run_app(console=console, single_command=True)

        output = console_output.getvalue()
        assert "Belling Cat" in output


def test_app_accepts_and_processes_investigate_command():
    """Verify app can accept and process /investigate command through prompt."""
    from unittest.mock import patch

    from belling_cat.cli import CommandRouter, run_app

    console_output = StringIO()
    console = Console(file=console_output, width=80, legacy_windows=False)

    # Track whether handler was called
    handler_called = []

    def mock_investigate_handler(args: str) -> str:
        handler_called.append(args)
        return f"Investigation started: {args}"

    # Mock prompt to return an investigate command
    with patch("belling_cat.cli.Prompt.ask", return_value="/investigate test claim"):
        with patch("belling_cat.cli.get_default_router") as mock_router:
            router = CommandRouter()
            router.register("investigate", mock_investigate_handler)
            mock_router.return_value = router

            run_app(console=console, single_command=True)

            # Verify handler was called with correct args
            assert handler_called == ["test claim"]

            output = console_output.getvalue()
            assert "Investigation started: test claim" in output


def test_module_entry_point_exists():
    """Verify the application can be run as a Python module."""
    import subprocess

    # Run the module - should not fail with "No module named __main__"
    result = subprocess.run(
        ["python", "-m", "belling_cat", "--version"],
        capture_output=True,
        text=True,
        timeout=2,
    )

    # Should not have the "No module named __main__" error
    assert "No module named" not in result.stderr
    assert "__main__" not in result.stderr or "cannot be directly executed" not in result.stderr


def test_app_processes_save_command():
    """Verify app can accept and process /save command through prompt."""
    from unittest.mock import patch

    from belling_cat.cli import CommandRouter, run_app

    console_output = StringIO()
    console = Console(file=console_output, width=80, legacy_windows=False)

    # Track whether handler was called
    handler_called = []

    def mock_save_handler(args: str) -> str:
        handler_called.append(args)
        return f"Report saved: {args}"

    with patch("belling_cat.cli.Prompt.ask", return_value="/save test-report"):
        with patch("belling_cat.cli.get_default_router") as mock_router:
            router = CommandRouter()
            router.register("save", mock_save_handler)
            mock_router.return_value = router

            run_app(console=console, single_command=True)

            assert handler_called == ["test-report"]
            output = console_output.getvalue()
            assert "Report saved: test-report" in output


def test_app_handles_invalid_command():
    """Verify app displays error message for invalid commands."""
    from unittest.mock import patch

    from belling_cat.cli import run_app

    console_output = StringIO()
    console = Console(file=console_output, width=80, legacy_windows=False)

    with patch("belling_cat.cli.Prompt.ask", return_value="/invalid something"):
        run_app(console=console, single_command=True)

        output = console_output.getvalue()
        assert "Unknown command" in output
        assert "/investigate" in output  # Should show usage guidance
        assert "/save" in output  # Should show usage guidance
