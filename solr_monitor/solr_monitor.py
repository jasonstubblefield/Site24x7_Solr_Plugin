#!/usr/bin/env python3

import requests
import json

# Configuration
SOLR_URL = "http://localhost:8983"
SOLR_CORES_STATUS_API = "/solr/admin/cores?action=STATUS"
PLUGIN_VERSION = "3"

def get_solr_cores_status():
    response = requests.get(SOLR_URL + SOLR_CORES_STATUS_API)
    if response.status_code == 200:
        return response.json()
    return None

def main():
    cores_data = get_solr_cores_status()

    output = {
        "plugin_version": PLUGIN_VERSION
    }
    units = {}

    # Check if we got a valid response
    if cores_data and 'status' in cores_data:
        output["status"] = 1  # 1 implies success, 0 implies failure
        output["msg"] = "Success"
        for core_name, core_info in cores_data['status'].items():
            # Get number of documents for each core
            doc_count_key = f"{core_name}_doc_count"
            doc_status_key = f"{core_name}_status"

            doc_count = core_info['index']['numDocs']

            output[doc_count_key] = doc_count
            output[doc_status_key] = 1  # Assuming the core is up if we got this far

            # Add units
            units[doc_count_key] = "documents"
            units[doc_status_key] = "status"

        # Add units dictionary to output
        output["units"] = units

        print(json.dumps(output, indent=4))
    else:
        # Print an error message if unable to fetch data
        print(json.dumps({
            "status": 0,
            "msg": "Failed to fetch Solr core status",
            "plugin_version": PLUGIN_VERSION
        }, indent=4))

if __name__ == '__main__':
    main()