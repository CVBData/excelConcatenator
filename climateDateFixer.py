# import the required modules
import pandas as pd

# disabled choose-your-own-path method
# pre_root = input("Please type in directory path to excel file containing dates to be fixed, "
#                 "followed by the enter key:")
# pre_outfile_name = input("Please type in name of excel file to be output, followed by the enter key:")

# hard-coded paths
pre_root = 'C:\\Users\\Richard.Bankoff\\Box\\Centre ValBio\\Centre ValBio Incoming Data\\Climate\\dataCleaningFolder\\climate_out2.csv'
pre_outfile_name = 'C:\\Users\\Richard.Bankoff\\Box\\Centre ValBio\\Centre ValBio Incoming Data\\Climate\\dataCleaningFolder\\climate_date_fixed2.csv'

# clean up leading/trailing whitespace - unnecessary for hard-coded variables, but good to leave in just in case
root = pre_root.strip()
outfile_name = pre_outfile_name.strip()

# definitions of months
months_with_28 = [2]
months_with_30 = [9, 4, 6, 11]
months_with_31 = [1, 3, 5, 7, 8, 10, 12]

# keep track of where we are in the dataframe (line_counter)
# and how many erroneous date fields there are (exception_counter)
line_counter = 0
exception_counter = 0

# open concatenated climate data for reading
file_for_date_cleanup = pd.read_csv(root)

# for each timestamp in climate file
for x in file_for_date_cleanup['TIMESTAMP']:
    # if there isn't the expected character "-" in the timestamp
    if '-' not in x:
        # increment the exception counter
        exception_counter = exception_counter + 1
        # retrieve the previous timestamp
        last_time = file_for_date_cleanup['TIMESTAMP'][line_counter-1]
        # split the date and time apart from previous timestamp
        last_date = last_time.split(' ')[0]
        # define next time - always 12AM, because that's where this error happens
        next_time = "00:00:00"

        # split up various components of previous date
        last_year = last_date.split('-')[0]
        last_month = last_date.split('-')[1]
        last_day = last_date.split('-')[2]

        # set date components as integers
        last_year = int(last_year)
        last_month = int(last_month)
        last_day = int(last_day)

        # leap year handling logic - if modulo 4 is 0, it's a leap year, unless it's
        # a century year, in which case it's not -- unless it's a century year divisible
        # by modulo 400, such as the year 2000, in which case it is.
        is_leap_year = False
        if last_year % 4 == 0:
            if last_year % 100 == 0:
                if last_year % 400 == 0:
                    is_leap_year = True
            else:
                is_leap_year = True

        # dummy variables for fixing date
        next_year = ''
        next_month = ''
        next_day = ''

        # if the previous timestamp was for a day before the 28th, just increment the day
        if last_day < 28:
            next_day = last_day + 1
            next_month = last_month
            next_year = last_year

        # if the previous timestamp was the 28th, check if it is February. If it is, check if it is
        # a leap year and increment accordingly; otherwise, just increment day to 29
        if last_day == 28:
            if last_month in months_with_28:
                if is_leap_year is True:
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

        # if the previous timestamp was the 29th, if it is February the next day is March 1st;
        # otherwise it is the 30th of the previous timestamp's month
        if last_day == 29:
            if last_month in months_with_28:
                next_day = 1
                next_month = 3
                next_year = last_year
            else:
                next_day = 30
                next_month = last_month
                next_year = last_year

        # if the previous timestamp was 30, check what month it was to determine whether to
        # proceed to 31 or to roll the month over
        if last_day == 30:
            if last_month in months_with_30:
                next_day = 1
                next_month = last_month + 1
                next_year = last_year
            else:
                next_day = 31
                next_month = last_month
                next_year = last_year

        # if the previous timestamp was the 31st, determine if it is December. If so, set the
        # following month to January, the day to the first, and increment the year; otherwise,
        # just increment the month and set the day to 1
        if last_day == 31:
            if last_month == 12:
                next_day = 1
                next_month = 1
                next_year = last_year + 1
            else:
                next_day = 1
                next_month = last_month + 1
                next_year = last_year
        # configure output as string with leading zeros for single-digit days and months
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

        # assemble the newly constructed date into the proper format:
        # "YYYY-MM-DD OO:OO:OO"
        parts_for_next_date = [next_year, next_month, next_day]
        next_date = "-".join(parts_for_next_date)
        parts_for_next_timestamp = [next_date, next_time]
        next_timestamp = " ".join(parts_for_next_timestamp)

        # print some checks for validation
        print(last_time)
        print(next_timestamp)
        print(last_date)

        # replace the previous erroneous value with the corrected timestamp
        file_for_date_cleanup['TIMESTAMP'][line_counter] = next_timestamp

    # increment the line counter
    line_counter = line_counter + 1

# print number of erroneous values detected
print(exception_counter)

# remove all duplicate lines from output dataframe
file_for_date_cleanup = file_for_date_cleanup.drop_duplicates()

# export the dataframe into a CSV file with specified name. CSV is used for output because
# large datasets may exceed the Excel spreadsheet specification; if you know your dataset is small
# enough to be put into .xlsx format, replace to_csv() with to_excel on the line below
file_for_date_cleanup.to_csv(outfile_name, index=False)

# exit
exit()
