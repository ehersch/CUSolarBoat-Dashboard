import json

# Load the JSON data from file
with open('/Users/tasmin/Documents/GitHub/2122CUSBSyscoRepo/Dashboard/data.json') as f:
    data = json.load(f)

# Extract voltage readings from JSON
readings = data['logs'][-1]['Readings']
labels = [reading['Timestamp'] for reading in readings]
v1Data = [reading['V1'] for reading in readings]


