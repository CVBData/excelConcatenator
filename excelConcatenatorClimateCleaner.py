# importing the required modules
import pandas as pd

# disabled choose-your-own-path method
# pre_root = input("Please type in directory path to excel file containing list of excel files to be concatenated, "
#                 "followed by the enter key:")
# pre_outfile_name = input("Please type in name of excel file to be output, followed by the enter key:")
# pre_variable_file = input("Please enter the path to an excel file with the acceptable variable fields stored in the"
#                          " first column, followed by the enter key:")

# hard-coded paths
pre_root = 'C:\\Users\\Richard.Bankoff\\Box\\Centre ValBio\\Centre ValBio Incoming Data\\Climate\\dataCleaningFolder\\List_of_excel_spreadsheet_locations_climate.xlsx'
pre_outfile_name = 'C:\\Users\\Richard.Bankoff\\Box\\Centre ValBio\\Centre ValBio Incoming Data\\Climate\\dataCleaningFolder\\climate_out2.csv'
pre_variable_file = 'C:\\Users\\Richard.Bankoff\\Box\\Centre ValBio\\Centre ValBio Incoming Data\\Climate\\dataCleaningFolder\\List_of_variables_climate.xlsx'

# clean up leading/trailing whitespace - unnecessary for hard-coded variables, but good to leave in just in case
root = pre_root.strip()
outfile_name = pre_outfile_name.strip()
variable_file = pre_variable_file.strip()

# read in list of Excel files for concatenation
file_list_manifest = pd.read_excel(root)
pre_variable_list = pd.read_excel(variable_file)

variable_list = pre_variable_list['variableNames'].tolist()

# check statements for verifying list of variables
print(variable_list)
print(len(variable_list))

# create list of all Excel files to be concatenated
file_list = file_list_manifest['fullPath'].tolist()

# list of Excel files we want to merge.
# pd.read_excel(file_path) reads the Excel
# data into pandas dataframe.
excl_list = []

# skip headers that are not useful
for file in file_list:
    excl_list.append(pd.read_excel(file, skiprows=[0, 2, 3]))

# create a new dataframe to store the
# merged Excel file.
excl_merged = pd.DataFrame()

# for each Excel file, clean data and append to list
for excl_file in excl_list:

    excl_file = excl_file.dropna(axis='columns', how='all')
    excl_file = excl_file.drop(['AirTC_3_Avg', 'AirTC_3_Std', 'RH_3'], axis=1, errors='ignore')
    excl_file = excl_file[variable_list]
    column_numbers = len(excl_file.columns)

    # if the number of columns is not what is expected, throw an error
    if column_numbers != 23:
        print("Missing column!")

    # appends the data into the excl_merged
    # dataframe.
    excl_merged = pd.concat([excl_merged, excl_file])

# exports the dataframe into a CSV file with
# specified name. CSV is used for output because
# large datasets may exceed the Excel spreadsheet
# specification; if you know your dataset is small
# enough to be put into .xlsx format, replace
# to_csv() with to_excel on the line below
excl_merged = excl_merged.dropna(axis='rows', how='all')
excl_merged.to_csv(outfile_name, index=False)
exit()
