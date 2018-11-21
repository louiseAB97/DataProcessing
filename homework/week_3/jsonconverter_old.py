import csv
import json


INFILE = 'weer.txt'

with open(INFILE, newline='') as f:
    reader = csv.reader(f)
    outfile = open('weeroutfile.json','w')
    for row in reader:
        clean_row = []
        if row[0].startswith('#'):
            continue
        for x in row:
            x = x.strip()
            clean_row.append(x)
        # Parse the CSV into JSON
        # the range of row[index] may vary depending on which columns you wish to include
        out = json.JSONEncoder().encode({clean_row[0]: clean_row[1: ]})
        outfile.write(out)
    # Save the JSON
    outfile.close()
