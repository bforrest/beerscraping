import csv, json

filename = "2012-national-finals.csv"

with open(filename) as f:
    reader = csv.DictReader(f)
    data = [r for r in reader]

for d in data:
    print(d)