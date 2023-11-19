from flask import Blueprint, jsonify
import os
import pandas as pd
import json

# Get the directory of the currently executing script
dir_path = os.path.dirname(os.path.realpath(__file__))

# Go up one level from the current script's directory
parent_dir = os.path.dirname(dir_path)

# Construct the path to the 'data/measurements/' directory
traceroute_measurements_dir = os.path.join(parent_dir, 'data', 'traceroute_measurement_results')


data_api = Blueprint('data_api', __name__)

@data_api.route('/traceroute_data', methods=['GET'])
def get_traceroute_dataframe():
    json_data_union = []
    for f in os.listdir(traceroute_measurements_dir):
        if f.endswith('.json'):
            with open(os.path.join(traceroute_measurements_dir, f)) as json_file:
                data = json.load(json_file)  # Parse the JSON file into a Python object
                if isinstance(data, list):
                    json_data_union.extend(data)  # Extend the list with the contents of this file
                else:
                    json_data_union.append(data)  # Append the object itself if it's not a list
    return pd.DataFrame(json_data_union)
