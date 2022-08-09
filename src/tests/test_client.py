"""Tests for client."""
from unittest import TestCase
from unittest.mock import Mock, call, patch

from src.client import GrafanaAPIClient


class TestClient(TestCase):
    @patch("src.client.get")
    def test_grafana_request(self, mock_get):
        """Test we can make call to Grafana API."""
        logger_mock = Mock()
        client = GrafanaAPIClient(hostname="localhost", port=42, logger=logger_mock)
        client._grafana_request("/path/api")
        self.assertTrue(
            call(
                "https://localhost:42/path/api",
                headers={"Accept": "application/json"},
                timeout=1,
            )
            in mock_get.mock_calls
        )
        client.bearer_token = "test_token"
        client._grafana_request("/path/api")
        self.assertTrue(
            call(
                "https://localhost:42/path/api",
                headers={
                    "Accept": "application/json",
                    "Authorization": "Bearer " + client.bearer_token,
                },
                timeout=1,
            )
            in mock_get.mock_calls
        )
