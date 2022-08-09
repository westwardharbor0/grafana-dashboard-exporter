# grafana-dashboard-exporter
Simple tool to export all or given dashboards to structure of JSON files

# Requirements
To run this beast you will need [`poetry`](https://python-poetry.org/). 
Poetry can be installed trough `pip` by `pip3 install poetry`.

# Usage
There are only two required arguments `--hostname` and `--port` to connect to Grafana API. 
The rest is optional
```
usage: exporter [-h] --hostname HOSTNAME --port PORT [--uid-filter UID_FILTER [UID_FILTER ...]] [--use-uid] [--use-https] [-d] [-p PATH]

optional arguments:
  -h, --help            show this help message and exit
  --hostname HOSTNAME   hostname of Grafana API running on
  --port PORT           port of Grafana API running on
  --uid-filter UID_FILTER [UID_FILTER ...]
                        list of Dashboard UIDs we will export
  --use-uid             use the UID in filename instead of title
  --use-https           use HTTPS for the Grafana API requests
  -d, --debug           increase logging verbosity to debug
  -p PATH, --path PATH  path to destination folder we save the dashboards
  ```
Example run
```
exporter --hostname "localhost" --port 4242 --use-https // This will export all dashboards to ./exports folder

exporter --hostname "localhost" --port 4242 --use-https --uid-filter ID1 ID2 ID3 ID4 --path ./dashboards // Will export dashboards with given UIDs to given folder
```
