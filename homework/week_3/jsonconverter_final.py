import pandas as pd
import csv
import json


INFILE = "weer.txt"
CSVFILE = "infileto.csv"
OUTFILE = "data.json"



with open(INFILE, newline='') as f:
    reader = csv.reader(f)
    station_dict = {}
    # key = station[row[0]], value = date_dict
    date_dict = {}
    # key = date (row[1]), value = dictionary with key value pairs (row[2:4])
    for row in reader:
        if row[0].startswith('#'):
            #  skip all comments
            continue
        date = row[1].strip()
        values_dict = {}
        # each date has its own key value pairs (measurements)
        values_dict['FHX'] = row[2].strip()
        values_dict['TX'] = row[3].strip()
        values_dict['DR'] = row[4].strip()
        date_dict[date] = values_dict
        station = row[0].strip()
        # append the date dictionary to the right station
        station_dict[station] = date_dict



with open(OUTFILE, 'w') as j:
    # convert dictionary to jsonfile
    json.dump(station_dict, j)







#
# with open(CSVFILE, 'w', newline='') as c:
#     fieldnames = ['STN', 'date', 'FHX', 'TX', 'DR']
#     writer = csv.DictWriter(c, fieldnames=fieldnames)
#     writer.writeheader()
#
#         writer.writerow(dict)
#         print("kaas")




#
# df = pd.read_csv(dict_list)
# outfile = open(OUTFILE,'w')
# outfile.write(df.to_json(orient='index'))
# outfile.close()
