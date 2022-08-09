"""Runnable."""
from src.main import GrafanaDashboardExporter


def main():
    """Run the export."""
    exporter = GrafanaDashboardExporter()
    exporter.run()


if __name__ == "__main__":
    main()
