import pandas as pd
import os
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
import re
import zipfile
from lxml import etree


''' ---------------Define Variables----------------'''
# URL of the website to scrape
url = 'https://bulkdata.uspto.gov/data/trademark/dailyxml/applications/'

pattern = re.compile(r'^apc2401\d{2}\.zip$') # only jan mon of 2024
path_base = 'data/xml_files_zip'
extracted_path_base = 'data/xml_files'
output_csv_path = 'data/csv_files'

''' --------------Define Functions----------------'''

def unzip_file(zip_file_path, dest_folder):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(dest_folder)
    
def extract_info_from_large_xml(xml_file_path):
    filename = os.path.basename(xml_file_path)
    context = etree.iterparse(xml_file_path, events=('end',), tag='case-file')
    data = []

    for event, elem in context:
        case_file_data = {}
        
        # Extract category code (international-code in classification)
        classification_elem = elem.find('classifications/classification/international-code')
        if classification_elem is not None:
            #if classification_elem.text == '003' or classification_elem.text == '004':
            case_file_data['category-code'] = classification_elem.text

            #extract mark-identification
            mark_identification_elem = elem.find('case-file-header/mark-identification')
            if mark_identification_elem is not None:
                case_file_data['mark-identification'] = mark_identification_elem.text
    
            # Extract serial number
            serial_number_elem = elem.find('serial-number')
            if serial_number_elem is not None:
                case_file_data['serial-number'] = serial_number_elem.text
            
            owners = elem.findall('case-file-owners/case-file-owner')
            party_names = []
            for owner in owners:
                party_name_elem = owner.find('party-name')
                if party_name_elem is not None:
                    party_names.append(party_name_elem.text)
            case_file_data['Case-File-Owners'] = ', '.join(party_names) 
            
            # Extract status code
            status_elem = elem.find('case-file-header/status-code')
            if status_elem is not None:
                case_file_data['status'] = status_elem.text
            
            case_file_data['xml_filename'] = filename

        if case_file_data:
            data.append(case_file_data)
        
        # Clear the element to free memory
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]

    return data

def process_xml_files_to_dataframe(xml_files,extracted_path):
    all_data = []
    
    for filename in tqdm(xml_files, desc="Processing XML files"):
        xml_file_path = os.path.join(extracted_path, filename)
        file_data = extract_info_from_large_xml(xml_file_path)
        all_data.extend(file_data)
    # Create a DataFrame from the aggregated data
    df = pd.DataFrame(all_data)
    return df

def save_dataframe_to_csv(df, output_csv_path):
    path = os.path.join(output_csv_path, f"trademarks.csv")
    # Write the DataFrame to a CSV file
    df.to_csv(path, index=False)


''' -------------Main Code-----------------'''

# Send a GET request to the website
response = requests.get(url)

if response.status_code == 200:
    print(f" Status code: {response.status_code}")
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all <a> tags
    links = soup.find_all('a')
    if not os.path.exists(path_base):
        os.makedirs(path_base)

    # Filter and collect links whose names match the specified pattern
    apc_links = [url + link.get('href') for link in links if pattern.match(link.get('href'))]
    # Download each file
    for link in tqdm(apc_links, desc="Downloading zipped files"):
        file_name = link.split('/')[-1]
        file_response = requests.get(link)
        if file_response.status_code == 200:
            with open(os.path.join(path_base, file_name), 'wb') as file:
                file.write(file_response.content)
        else:
            print(f"Failed to download {file_name}. Status code: {file_response.status_code}")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

print('~~~~~~~~~~~~~zipped files downloaded!')

#extract zipped files
zip_files = [f for f in os.listdir(path_base) if f.endswith('.zip')]
for zip_file in tqdm(zip_files, desc="Extracting zipped files"):
    zip_file_path = os.path.join(path_base, zip_file)
    unzip_file(zip_file_path, extracted_path_base)

print('~~~~~~~~~~~~~zipped files extracted!')


# Process XML files and get the DataFrame
xml_files = [f for f in os.listdir(extracted_path_base) if f.endswith('.xml')]
print(f"Number of XML files: {len(xml_files)}")
#split xml_files into 2 halves
xml_files1 = xml_files[:len(xml_files)//2]
xml_files2 = xml_files[len(xml_files)//2:]

print('1st half WIP')
df1 = process_xml_files_to_dataframe(xml_files1,extracted_path_base)

print('2nd half WIP')
df2 = process_xml_files_to_dataframe(xml_files2,extracted_path_base)
# Combine the two DataFrames
df = pd.concat([df1, df2], ignore_index=True)
print('Done! saving to csv')
save_dataframe_to_csv(df, output_csv_path)

# delete contents of extracted folder
for f in os.listdir(path_base):
    os.remove(os.path.join(path_base, f))

#delete zipped files
for f in os.listdir(extracted_path_base):
    os.remove(os.path.join(extracted_path_base, f))

print('~~~~~~~~~~~~~cleaned up!')