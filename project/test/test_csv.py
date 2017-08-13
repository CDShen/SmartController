import csv

with open('../data/plan.csv') as f:
    f_csv = csv.DictReader(f)
    for r in f_csv:
        print(r.get('Name'))
