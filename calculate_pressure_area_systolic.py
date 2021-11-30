# Purpose: Calculates the area under the blood pressure curves (SYSTOLIC ONLY)
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

####### CONSTANTS #######

CSV_OUT_FILENAME = 'area_log.csv' # CSV file name of output log

PIXELS_PER_SQUARE = 1000
AREA_PER_SQUARE = 50
AREA_PER_PIXEL = AREA_PER_SQUARE / PIXELS_PER_SQUARE

MINUTES_PER_UNIT_LENGTH = 5
PIXELS_PER_LENGTH = 30

HEIGHT_CUT_OFF = 50

#########################

out = open(CSV_OUT_FILENAME, 'w', newline='')
csv_out = csv.writer(out)
csv_out.writerow(['redcap_number', 'area']) # Titles in CSV file

sum_of_lengths = 0
num_patients = 0

for file in os.listdir():
    num_patients += 1
    if (file.endswith('.csv') and file != CSV_OUT_FILENAME):
        with open(file, newline='') as csv_file:
            csv_file.readline() # skips first row in CSV (contains column headers)
            num_pixels = 0
            time_pixels = 0
            for row in csv_file:
                if float(row.split(',')[6].strip()) == 0:
                    num_pixels += float(row.split(',')[1].strip()) # 2nd column in CSV is area
                else:
                    time_pixels += float(row.split(',')[6].strip()) # 7th column in CSV is length
                    sum_of_lengths += (time_pixels / PIXELS_PER_LENGTH) * MINUTES_PER_UNIT_LENGTH

            area_cut_off = (time_pixels / PIXELS_PER_LENGTH) * MINUTES_PER_UNIT_LENGTH * HEIGHT_CUT_OFF
            area = (num_pixels * AREA_PER_PIXEL) + area_cut_off # FINAL AREA VALUE

            # Write data to CSV
            if csv_file.name.find("_new") == -1:
                csv_out.writerow([csv_file.name[0: csv_file.name.find("_resultats")], area])
                print("RedCap #:", csv_file.name[0: csv_file.name.find("_resultats")], "\tArea:", area, "\n")
            else:
                csv_out.writerow([csv_file.name[0: csv_file.name.find("_new")], area])
                print("RedCap #:", csv_file.name[0: csv_file.name.find("_new")], "\tArea:", area, "\n")

average_duration = sum_of_lengths / num_patients # calculate average duration of surgery
csv_out.writerow(["Average duration", average_duration])


out.close()