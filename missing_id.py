import csv


def filter_listings(input_file, output_file):
    housing_ids = set()  # To store unique housing IDs

    with open(input_file, 'r', newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)  # Assuming tab-delimited data

        for row in reader:
            # Check if the row contains "(Agreement required)" or "(Sign-in required)" in either 'price' or 'price_sold' attribute
            if '(Agreement required)' in row or '(Sign-in required)' in row:
                housing_id = row[
                    0]  # Assuming the housing ID is in the first column
                housing_ids.add(housing_id)

    with open(output_file, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        # writer.writerow(['Housing ID'])  # Write a header row
        for housing_id in housing_ids:
            writer.writerow([housing_id])


# # Specify the path to your input CSV file and the desired output CSV file
# input_file_path = 'A:/(000) Research Assistant/RA code/listing_details_type6_updated.csv'
# output_file_path = 'A:/(000) Research Assistant/RA code/missing_id_ALL_type/missing_ids_type6.csv'
#
# # Call the function to filter and isolate the housing IDs as a CSV file
# filter_listings(input_file_path, output_file_path)
# print(f'Filtered housing IDs written to "{output_file_path}"')



# FINDING THE EXISTING DATA

input_file = 'A:/(000) Research Assistant/RA code/listing_details_type3_7_updated.csv'
output_file = 'A:/(000) Research Assistant/existing data/existing_type3_7.csv'

with open(input_file, 'r', newline='', encoding='utf-8') as csvfile_in, open(output_file, 'w', newline='', encoding='utf-8') as csvfile_out:
    reader = csv.reader(csvfile_in)
    writer = csv.writer(csvfile_out)

    # Iterate through rows in the existing CSV file
    for row in reader:
        # Check if the row contains the unwanted text
        if "(Sign-in required)" not in row and "(Agreement required)" not in row:
            # If the row does not contain the unwanted text, write it to the new CSV file
            writer.writerow(row)
