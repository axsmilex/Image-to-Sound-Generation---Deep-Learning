import pandas as pd


def merge_csv_files(file1, file2, output_file):
    # Read CSV files into pandas dataframes without header
    df1 = pd.read_csv(file1, header=None)
    df2 = pd.read_csv(file2, header=None)

    # Merge dataframes based on the specified column index
    merged_df = pd.merge(df1, df2, left_on=df1.columns[0], right_on=df2.columns[1], how='inner')
    merged_df = merged_df.iloc[:, 2:]

    # Write merged dataframe to a new CSV file
    merged_df.to_csv(output_file, index=False, header=False)


# Specify the paths to your CSV files and the output file
file1_path = 'A:/(000) Research Assistant/RA code/missing_id_all_type/missing_ids_type3_7.csv'
file2_path = 'A:/(000) Research Assistant/RA code/house_ids_list_type3.csv'
output_file_path = 'A:/(000) Research Assistant/RA code/json_missing3/merged_type3_7.csv'

# Call the merge function
merge_csv_files(file1_path, file2_path, output_file_path)
print(f'Merged data written to "{output_file_path}"')


def remove_duplicates_by_column(input_file, output_file, column_index):
    # Read input CSV file and filter out duplicates
    df = pd.read_csv(input_file, header=None)
    df.drop_duplicates(subset=[column_index], inplace=True)

    # Write cleaned data to output CSV file
    df.to_csv(output_file, index=False, header=False)


input_file_path = 'A:/(000) Research Assistant/RA code/json_missing3/merged_type3_7.csv'
output_file_path = 'A:/(000) Research Assistant/RA code/json_missing3/cleaned_merged_3_7.csv'
id_column_index = 1  # Index of the column with IDs (0-based)

# Call the function to remove duplicates
remove_duplicates_by_column(input_file_path, output_file_path, id_column_index)
print(f'Duplicates removed, cleaned data written to "{output_file_path}"')
