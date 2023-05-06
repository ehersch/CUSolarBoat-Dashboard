import json
import matplotlib.pyplot as plt
from subprocess import run

while True:
    with open('./data.json') as f:
        data = json.load(f)

    readings = data['logs'][-1]['Readings']
    labels = [reading['Timestamp'] for reading in readings]
    v1Data = [reading['V1'] for reading in readings]
    v2Data = [reading['V2'] for reading in readings]
    v3Data = [reading['V3'] for reading in readings]

    x_pos = [0, 1, 2]
    voltage_values = [v1Data[-1], v2Data[-1], v3Data[-1]]
    plt.bar(x_pos, voltage_values)
    plt.xticks(x_pos, ['V1', 'V2', 'V3'])
    plt.yticks(range(0, 101, 10))
    plt.title('Voltage Readings')
    plt.xlabel('Voltage Reading')
    plt.ylabel('Voltage')
    for i, v in enumerate(voltage_values):
        plt.text(i, v+1, str(v), ha='center', fontweight='bold')

    plt.show()

    run(["node", "httpget.js"])

