# Purpose: Calculates the area under the blood pressure curves (DIASTOLIC ONLY)
#
# Anindro Bhattacharya
#
# Preconditions:
#  - size of each square in grid is 1000 pixels
#  - 1 square = 10 mm Hg * 5 min = 50 mm Hg*min
#     ==> Unit for final area: mm Hg * min
#  - length of 1 square = 30 pixels
#
# Note: Entries in final CSV are not in numerical order by RedCap number
#       This must be done manually using the Sort function in Excel or
#       any other spreadsheet software.
#

####### IMPORTS #######

import os
import csv
import pandas as pd

####### CONSTANTS #######

CSV_OUT_FILENAME = 'area_log_diastolic.csv' # CSV file name of output log
LENGTH = 'length'
LENGTHS_FILE = 'pressure_lengths.csv'

PIXELS_PER_SQUARE = 1000
AREA_PER_SQUARE = 50
AREA_PER_PIXEL = AREA_PER_SQUARE / PIXELS_PER_SQUARE

MINUTES_PER_UNIT_LENGTH = 5
PIXELS_PER_LENGTH = 30

HEIGHT_CUT_OFF = 50

#########################

lengths_df = pd.read_csv(LENGTHS_FILE, index_col='redcap_number')

out = open(CSV_OUT_FILENAME, 'w', newline='')
csv_out = csv.writer(out)
csv_out.writerow(['redcap_number', 'diastolic_area']) # Titles in CSV file

for file in os.listdir():
    if (file.endswith('.csv') and file != CSV_OUT_FILENAME and 'resultats_diastolique' in file):
        with open(file, newline='') as csv_file:
            csv_file.readline() # skips first row in CSV (contains column headers)
            num_pixels = 0
            print(file)
            for row in csv_file:
                num_pixels += float(row.split(',')[1].strip()) # 2nd column in CSV is area
                
            time_pixels = lengths_df.at[int(csv_file.name[0: csv_file.name.find("_")]), LENGTH]
            area_cut_off = (time_pixels / PIXELS_PER_LENGTH) * MINUTES_PER_UNIT_LENGTH * HEIGHT_CUT_OFF
            area = (num_pixels * AREA_PER_PIXEL) + area_cut_off # FINAL AREA VALUE

            # Write data to CSV
            csv_out.writerow([csv_file.name[0: csv_file.name.find("_")], area])
            print("RedCap #:", csv_file.name[0: csv_file.name.find("_resultats")], "\tArea:", area, "\n")

out.close()