from more_itertools import batched
import csv

input_file = 'A:/(000) Research Assistant/existing data/existing_type3_7.csv'
output_file = 'A:/(000) Research Assistant/existing data/existing_type3_7_updated.csv'

temp_list = []
result = {'id_listing:': [], 'seo_address:': [], 'seo_suffix:': [],
          'price:': [], 'price_sold:': [], 'house_type_name:': [],
          'address:': [], 'list_dates:': [], 'id_municipality:': [],
          'municipality_name:': [], 'bedroom:': [], 'text:': [],
          'Description:': []}

column_names = list(result.keys())

with open(input_file, 'r', newline='', encoding='utf-8') as csvfile_in, open(
        output_file, 'w', newline='', encoding='utf-8') as csvfile_out:
    reader = csv.reader(csvfile_in)
    writer = csv.DictWriter(csvfile_out, fieldnames=column_names)

    writer.writeheader()
    for row in reader:
        for i in row:
            temp_list.append(i)

    for listing in batched(temp_list, 25):
        result['id_listing:'].append(listing[0])
        result['seo_address:'].append(listing[2])
        result['seo_suffix:'].append(listing[4])
        result['price:'].append(listing[6])
        result['price_sold:'].append(listing[8])
        result['house_type_name:'].append(listing[10])
        result['address:'].append(listing[12])
        result['list_dates:'].append(listing[14])
        result['id_municipality:'].append(listing[16])
        result['municipality_name:'].append(listing[18])
        result['bedroom:'].append(listing[20])
        result['text:'].append(listing[22])
        result['Description:'].append(listing[24])

    for i in range(len(result['id_listing:'])):
        row_data = {col_name: result[col_name][i] for col_name in
                    column_names}
        writer.writerow(row_data)
