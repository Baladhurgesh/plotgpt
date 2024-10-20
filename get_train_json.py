import os
import json

# Specify the folder containing the JSON files
folder_path = 'train_data'  # Update this to your folder path
final_json_path = 'identity.json'

# Initialize an empty list to hold the data
combined_data = []

# Iterate through all files in the specified folder
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        
        # Read each JSON file and append its content to the list
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            combined_data.append(data)

# Save the combined data to a single JSON file
with open(final_json_path, 'w') as final_json_file:
    json.dump(combined_data, final_json_file, indent=4)

