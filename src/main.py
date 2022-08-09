"""Wrapper to run the exporter."""
from argparse import ArgumentParser
from json import dump
from logging import DEBUG, INFO, Logger, basicConfig, getLogger
from pathlib import Path

from .client import GrafanaAPIClient
from .constants import DEFAULT_EXPORT_FOLDER_NAME, LOG_FORMAT, SERVICE_NAME


class GrafanaDashboardExporter:
    """Exporter using the client."""

    @staticmethod
    def get_cli_arguments() -> ArgumentParser:
        """Setup the argument parser."""
        parser = ArgumentParser()
        parser.add_argument(
            "--hostname",
            type=str,
            required=True,
            help="hostname of Grafana API running on",
        )
        parser.add_argument(
            "--port",
            type=str,
            required=True,
            help="port of Grafana API running on",
        )
        parser.add_argument(
            "--uid-filter",
            nargs="+",
            help="list of Dashboard UIDs we will export",
        )
        parser.add_argument(
            "--use-uid",
            action="store_true",
            default=False,
            help="use the UID in filename instead of title",
        )
        parser.add_argument(
            "--use-https",
            action="store_true",
            default=False,
            help="use HTTPS for the Grafana API requests",
        )
        parser.add_argument(
            "-d",
            "--debug",
            action="store_true",
            default=False,
            help="increase logging verbosity to debug",
        )
        parser.add_argument(
            "-p",
            "--path",
            type=Path,
            default=DEFAULT_EXPORT_FOLDER_NAME,
            help="path to destination folder we save the dashboards",
        )
        return parser

    @staticmethod
    def save_dashboard(path: Path, dashboard: dict):
        """Save dashboard to JSON file.

        :param path: Path to the destination file for content.
        :param dashboard: Data to be saved as JSON to file.
        """
        with open(path, "w") as file:
            dump(dashboard, file, indent=4)
            file.write("\n")

    @staticmethod
    def normalize_filename(filename: str) -> str:
        """Normalize the names of dashboard to be used as filenames.

        :param filename: Raw filename to be normalized.
        :return: Normalized filename.
        """
        return filename.replace(" ", "_").replace(".", "")

    @staticmethod
    def setup_logging(debug: bool = False) -> Logger:
        """Setup the logger for exporting.

        :param debug: Toggle to switch to more logging.
        :return: Instance of logger.
        """
        basicConfig(format=LOG_FORMAT)
        logger = getLogger(SERVICE_NAME)

        if debug:
            logger.setLevel(DEBUG)
        else:
            logger.setLevel(INFO)

        return logger

    def run(self):
        """Run the export."""
        arg_parser = self.get_cli_arguments()
        args = arg_parser.parse_args()
        logger = self.setup_logging()
        exporter = GrafanaAPIClient(
            hostname=args.hostname,
            port=args.port,
            debug=args.debug,
            scheme="https" if args.use_https else "http",
            logger=logger,
        )
        if not exporter.healthy_connection():
            logger.error(
                "We failed to establish healthy connection to Grafana API", extra={}
            )
            exit(2)
        # Check if we will load dashboards or just specific UIDs.
        if args.uid_filter:
            dashboard_list = [{"uid": uid} for uid in args.uid_filter]
        else:
            dashboard_list = exporter.get_dashboards_list()
        # Process the dashboard.
        for dashboard in dashboard_list:
            uid = dashboard["uid"]
            if (
                not (detail := exporter.get_dashboard(uid))
                or detail["meta"]["isFolder"]
            ):
                continue
            detail_json = detail["dashboard"]
            title = detail_json["title"]
            folder = dashboard.get("folderTitle", "")
            filename = uid if args.use_uid else title
            # Prepare and setup the base folder for dashboards.
            target_folder = args.path.joinpath(folder)
            target_folder.mkdir(parents=True, exist_ok=True)
            # Prepare the final path for storing the dashboard.
            path = target_folder.joinpath(
                self.normalize_filename(filename)
            ).with_suffix(".json")
            # Save the JSON to file.
            self.save_dashboard(path, detail_json)
