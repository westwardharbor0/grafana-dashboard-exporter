"""Tests for main."""
from pathlib import Path
from unittest import TestCase
from unittest.mock import call, patch

from src.constants import SERVICE_NAME
from src.main import GrafanaDashboardExporter


class TestMain(TestCase):
    def setUp(self):
        """Setup essentials for every test."""
        self.exporter: GrafanaDashboardExporter = GrafanaDashboardExporter()

    def test_setup_logger(self):
        """Test we setup logger."""
        logger = self.exporter.setup_logging(True)
        self.assertEqual(logger.level, 10)
        self.assertEqual(logger.name, SERVICE_NAME)

    def test_normalize_filename(self):
        """Test we can normalize string to be used as filename."""
        test_cases = (
            ("Test dashboard MF", "Test_dashboard_MF"),
            ("Test .json dashboard", "Test_json_dashboard"),
        )
        for test_case in test_cases:
            self.assertEqual(
                test_case[1], self.exporter.normalize_filename(test_case[0])
            )

    @patch("src.main.open")
    def test_save_dashboard(self, mock_open):
        """Test we save dict as json with new line on end."""
        test_json = {"json": "yes", "valid": 1}
        test_path = Path("/some/path/to/json/test.json")
        self.exporter.save_dashboard(test_path, test_json)
        self.assertTrue(call().__enter__().write("\n") in mock_open.mock_calls)
        self.assertTrue(call().__enter__().write('"json"') in mock_open.mock_calls)
        self.assertTrue(call().__enter__().write('"yes"') in mock_open.mock_calls)
        self.assertTrue(call().__enter__().write('"valid"') in mock_open.mock_calls)
        self.assertTrue(call().__enter__().write("1") in mock_open.mock_calls)
