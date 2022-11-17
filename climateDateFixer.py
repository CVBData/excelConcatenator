# importing the required modules
import pandas as pd

# disabled choose-your-own-path method
# pre_root = input("Please type in directory path to excel file containing dates to be fixed, "
#                 "followed by the enter key:")
# pre_outfile_name = input("Please type in name of excel file to be output, followed by the enter key:")

# hard-coded paths
pre_root = 'C:\\Users\\Richard.Bankoff\\Box\\Centre ValBio\\Centre ValBio Incoming Data\\Climate\\dataCleaningFolder\\climate_out2.csv'
pre_outfile_name = 'C:\\Users\\Richard.Bankoff\\Box\\Centre ValBio\\Centre ValBio Incoming Data\\Climate\\dataCleaningFolder\\climate_date_fixed.csv'

# clean up leading/trailing whitespace - unnecessary for hard-coded variables, but good to leave in just in case
root = pre_root.strip()
outfile_name = pre_outfile_name.strip()
months_with_28 = [2]
months_with_30 = [9, 4, 6, 11]
months_with_31 = [1, 3, 5, 7, 8, 10, 12]

leap_years = ["2000", "2004", "2008", "2012", "2016", "2020", "2024", "2028", "2032", "2036", "2040", "2044", "2048"]
# read in list of Excel files for concatenation
exception_counter = 0
line_counter = 0
file_for_date_cleanup = pd.read_csv(root)
for x in file_for_date_cleanup['TIMESTAMP']:
    # print(x)
    if '-' not in x:
        exception_counter = exception_counter + 1
        last_time = file_for_date_cleanup['TIMESTAMP'][line_counter-1]
        last_date = last_time.split(' ')[0]
        next_time = "00:00:00"
        last_year = last_date.split('-')[0]
        last_month = last_date.split('-')[1]
        last_day = last_date.split('-')[2]
        last_year = int(last_year)
        last_month = int(last_month)
        last_day = int(last_day)
        next_year = ''
        next_month = ''
        next_day = ''
        if last_day < 28:
            next_day = last_day + 1
            next_month = last_month
            next_year = last_year
        if last_day == 28:
            if last_month in months_with_28:
                if last_year in leap_years:
                    next_day = 29
                    next_month = last_month
                    next_year = last_year
                else:
                    next_day = 1
                    next_month = 3
                    next_year = last_year
            else:
                next_day = 29
                next_month = last_month
                next_year = last_year
        if last_day == 29:
            if last_month in months_with_28:
                next_day = 1
                next_month = 3
                next_year = last_year
            else:
                next_day = 30
                next_month = last_month
                next_year = last_year
        if last_day == 30:
            if last_month in months_with_30:
                next_day = 1
                next_month = last_month + 1
                next_year = last_year
            else:
                next_day = 31
                next_month = last_month
                next_year = last_year
        if last_day == 31:
            if last_month == 12:
                next_day = 1
                next_month = 1
                next_year = last_year + 1
            else:
                next_day = 1
                next_month = last_month + 1
                next_year = last_year
        if next_day < 10:
            next_day = str(next_day)
            next_day = "0"+next_day
        else:
            next_day = str(next_day)
        if next_month < 10:
            next_month = str(next_month)
            next_month = "0"+next_month
        else:
            next_month = str(next_month)

        next_year = str(next_year)
        parts_for_next_date = [next_year, next_month, next_day]
        next_date = "-".join(parts_for_next_date)
        parts_for_next_timestamp = [next_date, next_time]
        next_timestamp = " ".join(parts_for_next_timestamp)

        print(last_time)
        print(next_timestamp)
        print(last_date)
        file_for_date_cleanup['TIMESTAMP'][line_counter] = next_timestamp
    line_counter = line_counter + 1

print(exception_counter)
# exports the dataframe into a CSV file with
# specified name. CSV is used for output because
# large datasets may exceed the Excel spreadsheet
# specification; if you know your dataset is small
# enough to be put into .xlsx format, replace
# to_csv() with to_excel on the line below
# excl_merged.to_csv(outfile_name, index=False)
file_for_date_cleanup.to_csv(outfile_name, index=False)
exit()
