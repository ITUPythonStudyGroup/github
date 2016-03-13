import json

with open('frequencies.json', 'r') as f:
    frequencies = json.loads(f.read())
    frequencies = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
    for frequency in frequencies[:20]: print(frequency)
