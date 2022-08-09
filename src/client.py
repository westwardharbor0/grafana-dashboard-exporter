"""Exporter logic."""
from logging import Logger, getLogger
from typing import Optional, Union

from requests import get

from .constants import (
    API_CHECK_ENDPOINT,
    API_DETAIL_ENDPOINT,
    API_SEARCH_ENDPOINT,
    DEFAULT_REQUEST_TIMEOUT,
    SERVICE_NAME,
)


class GrafanaAPIClient:
    """Logic to export dashboards using Grafana API into file structure."""

    def __init__(
        self,
        hostname: str,
        port: int,
        bearer_token: str = "",
        debug: bool = False,
        scheme: str = "https",
        logger: Optional[Logger] = None,
    ):
        self.hostname = hostname
        self.port = port
        self.bearer_token = bearer_token
        self.debug = debug
        self.scheme = scheme
        self.logger: Logger = logger or getLogger(SERVICE_NAME)

    def _grafana_request(self, path: str) -> tuple[Union[dict, list], int]:
        """Make a request to Grafana API.

        :param path: Path to be called on Grafana API.
        :return: Result of the request with status code.
        """
        # Create the URL we will be calling.
        url = f"{self.scheme}://{self.hostname}:{self.port}{path}"
        headers = {
            "Accept": "application/json",
        }

        if self.bearer_token:
            headers["Authorization"] = f"Bearer {self.bearer_token}"
        # Try to call the URL for result.
        try:
            request = get(url, headers=headers, timeout=DEFAULT_REQUEST_TIMEOUT)
        except Exception as e:
            self.logger.error(
                "Failed to make request",
                extra={"context": {"url": url, "error": e}},
            )
            raise
        # Try to parse the response since we got some.
        try:
            return request.json(), request.status_code
        except Exception as e:
            self.logger.error(
                "Failed parse JSON from request response",
                extra={
                    "context": {
                        "url": url,
                        "response": request.text,
                        "status_code": request.status_code,
                        "error": e,
                    }
                },
            )

    def healthy_connection(self) -> bool:
        """Check if the connection to Grafana API is possible.

        :return: Bool if connection was successful.
        """
        response, status_code = self._grafana_request(API_CHECK_ENDPOINT)
        context = {
            "context": {
                "response": response,
                "status_code": status_code,
            }
        }
        if not response or response.get("database") != "ok" or status_code != 200:
            self.logger.error("Grafana API seems to be unhealthy", extra=context)
            return False
        self.logger.debug("Grafana API seems healthy", extra=context)
        return True

    def get_dashboard(self, uid: str) -> Optional[dict]:
        """Load the detail of the dashboard in dict format.

        :param uid: Identifier of the dashboard.
        :return: Dashboard detail in dict format.
        """
        detail_path = f"{API_DETAIL_ENDPOINT}{uid}"
        response, status_code = self._grafana_request(detail_path)
        context = {
            "context": {
                "response": response,
                "status_code": status_code,
            }
        }
        if status_code != 200:
            self.logger.error("Failed to load dashboard", extra=context)
            return None
        if not response.get("dashboard"):
            self.logger.error(
                "Loaded dashboard seems to be empty or broken", extra=context
            )
            return None
        return response

    def get_dashboards_list(self) -> Optional[list[dict]]:
        """List all the dashboards in grafana.

        :return: List of dashboards in dict format if request successful.
        """
        detail_path = f"{API_SEARCH_ENDPOINT}"
        response, status_code = self._grafana_request(detail_path)
        context = {
            "context": {
                "response": response,
                "status_code": status_code,
            }
        }
        if status_code != 200:
            self.logger.error("Failed to load dashboards list", extra=context)
            return None
        return response
