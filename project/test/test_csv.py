import csv
#
# with open('../data/plan.csv') as f:
#     f_csv = csv.DictReader(f)
#     for r in f_csv:
#         print(r.get('Name'))

with open('../data/flightplan{0}.csv'.format(1)) as f:
    f_csv = csv.DictReader(f)
    for r in f_csv:
        id = int(r.get('ID'))
        print(int(id))