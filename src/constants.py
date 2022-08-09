"""Storage for all the constants."""
from pathlib import Path

SERVICE_NAME = "grafana-dashboard-exporter"
# Definition of used endpoints.
API_BASE_URL = "/api"
API_SEARCH_ENDPOINT = f"{API_BASE_URL}/search"
API_DETAIL_ENDPOINT = f"{API_BASE_URL}/dashboards/uid/"
API_CHECK_ENDPOINT = f"{API_BASE_URL}/health"
# Defaults for arguments.
DEFAULT_REQUEST_TIMEOUT = 1
DEFAULT_EXPORT_FOLDER_NAME = Path("./exports")
# Format of logs.
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(context)s"
