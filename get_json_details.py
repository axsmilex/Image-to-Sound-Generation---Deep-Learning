import os
import json
import csv

folder_path = 'A:/(000) Research Assistant/RA code/json4_rrr'


def filter_json_file_names_with_detail(folder_paths):
    json_file_names = []

    for filename in os.listdir(folder_paths):
        if filename.endswith('.json') and 'detail' in filename.lower():
            json_file_names.append(filename)

    return json_file_names


def read_json_files(folder_paths, file_names):
    json_data_list = []

    for filename in file_names:
        file_path = os.path.join(folder_paths, filename)
        with open(file_path, 'r') as json_file:
            try:
                data = json.load(json_file)
                json_data_list.append(data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in {file_path}: {e}")

    return json_data_list


json_detail = filter_json_file_names_with_detail(folder_path)
json_data_list = read_json_files(folder_path, json_detail)


# The nested values that we want from the json data list of type 2
nested_value = ['id_listing', 'seo_address', 'seo_suffix', 'price',
                'price_sold',
                'house_type_name', 'address', 'list_dates', 'id_municipality',
                'municipality_name', 'bedroom', 'text']


def filter_category(data_list):
    filtered_json_data_list = []
    for json_data in data_list:
        # Adds all detail keys of the listing
        for key in nested_value:
            filtered_json_data_list.append(key + ":")
            filtered_json_data_list.append(json_data['data']['house'][key])
        # Add the descriptions of the listings
        filtered_json_data_list.append("Description:")
        filtered_json_data_list.append(json_data['data']['key_facts']['description1'])

    return filtered_json_data_list


# Split the entire list into separate chunks indicating the values of that listing
def split_list_by_id_listing(input_list):
    result_list = []
    current_sublist = []

    for item in input_list:
        if item == 'id_listing:':
            if current_sublist:
                result_list.append(current_sublist)
            current_sublist = []
        else:
            current_sublist.append(item)

    if current_sublist:
        result_list.append(current_sublist)

    return result_list


# Write the extracted data to a CSV file
def write_to_csv(data_list, csv_filename):
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        for row in data_list:
            csv_writer.writerow(row)


# Filter the json details files by categories
filtered_json_details = filter_category(json_data_list)

# All the details of json2 listing data files
listings_details = split_list_by_id_listing(filtered_json_details)

# Define the CSV file name
csv_filename = 'listing_details_type4_RRR_final.csv'

# Write the extracted and organized data to the CSV file
write_to_csv(listings_details, csv_filename)

print(f"Data has been written to {csv_filename}")



# # Find the ids of the listings that require signin to access price etc
# def find_signin_required(nested_list):
#     list_ids = []
#     for sublist in nested_list:
#         for item in sublist:
#             if '(Sign-in required)' or '(Agreement required)' in item:
#                 list_ids.append(sublist[0])
#     return list_ids
#
#
# def write_list_to_csv(data, filename):
#     with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
#         writer = csv.writer(csv_file)
#         for item in data:
#             writer.writerow([item])
#
#
# # Find all the ids that require sign-in or agreement to run 2_house_detail again
# signin_ids = find_signin_required(listings_details)
# # print(signin_ids)
# #
# filename = 'missing_signin_ids_type4.csv'
# write_list_to_csv(signin_ids, filename)
# print(f'CSV file "{filename}" created successfully.')



