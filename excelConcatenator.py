# importing the required modules
import pandas as pd


# csv files in the path
pre_root = input("Please type in directory path to excel file containing list of excel files to be concatenated, followed by the enter key:")
pre_outfile_name = input("Please type in name of excel file to be output, followed by the enter key:")

# clean up leading/trailing whitespace
root = pre_root.strip()
outfile_name = pre_outfile_name.strip()

# read in list of Excel files for concatenation
file_list_manifest = pd.read_excel(root)

file_list = file_list_manifest['fullPath'].tolist()
# list of Excel files we want to merge.
# pd.read_excel(file_path) reads the Excel
# data into pandas dataframe.
excl_list = []

for file in file_list:
    excl_list.append(pd.read_excel(file))

# create a new dataframe to store the
# merged Excel file.
excl_merged = pd.DataFrame()

for excl_file in excl_list:
    # appends the data into the excl_merged
    # dataframe.
    excl_merged = excl_merged.append(
        excl_file, ignore_index=True)

# exports the dataframe into Excel file with
# specified name.
excl_merged.to_csv(outfile_name, index=False)
exit()

