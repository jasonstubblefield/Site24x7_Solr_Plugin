#!/usr/bin/env python3
"""Site24x7 custom plugin that reports Apache Solr core health and document counts."""

import json
import os

import requests

# Override with the SOLR_URL environment variable if Solr is not local.
SOLR_URL = os.environ.get("SOLR_URL", "http://localhost:8983")
SOLR_CORES_STATUS_API = "/solr/admin/cores?action=STATUS"
REQUEST_TIMEOUT_SECONDS = 10

# Site24x7 detects changes by version number; bump in whole integers.
PLUGIN_VERSION = "4"


def get_solr_cores_status():
    try:
        response = requests.get(
            SOLR_URL + SOLR_CORES_STATUS_API, timeout=REQUEST_TIMEOUT_SECONDS
        )
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError):
        return None


def main():
    cores_data = get_solr_cores_status()

    if not cores_data or "status" not in cores_data:
        print(json.dumps({
            "status": 0,
            "msg": "Failed to fetch Solr core status",
            "plugin_version": PLUGIN_VERSION,
        }, indent=4))
        return

    output = {
        "plugin_version": PLUGIN_VERSION,
        "status": 1,  # 1 implies success, 0 implies failure
        "msg": "Success",
    }
    units = {}

    for core_name, core_info in cores_data["status"].items():
        doc_count_key = f"{core_name}_doc_count"
        doc_status_key = f"{core_name}_status"

        output[doc_count_key] = core_info["index"]["numDocs"]
        output[doc_status_key] = 1  # The core responded, so report it as up.

        units[doc_count_key] = "documents"
        units[doc_status_key] = "status"

    output["units"] = units
    print(json.dumps(output, indent=4))


if __name__ == "__main__":
    main()
