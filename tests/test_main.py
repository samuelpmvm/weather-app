import subprocess
import sys
import tempfile
import http.server
import threading
import os
import requests

def test_cli_help():
    """Test that the CLI help message is shown."""
    result = subprocess.run(
        [sys.executable, "-m", "weather_app", "--help"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "usage:" in result.stdout.lower()

def test_cli_invalid_api():
    """Test CLI with an invalid API base URL."""
    result = subprocess.run(
        [sys.executable, "-m", "weather_app", "Lisboa", "--api-base", "http://127.0.0.1:9999"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "Error connecting to API" in result.stdout or "Failed to establish a new connection" in result.stdout

def test_cli_missing_city():
    """Test CLI with missing required city argument."""
    result = subprocess.run(
        [sys.executable, "-m", "weather_app"],
        capture_output=True, text=True
    )
    assert result.returncode != 0
    assert "usage:" in result.stderr.lower() or "usage:" in result.stdout.lower()