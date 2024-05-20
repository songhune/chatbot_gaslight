import json

# The path to your input JSON file
input_file_path = './gaslighting_scripts2.json'
# The path for the output JSON Lines (JSONL) file
output_file_path = './output.jsonl'

# Read the JSON file
with open(input_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# The static part to prepend to each entry
static_part = {
    "role": "system",
    "content": "you are a sarcastic, narcissistic chatbot that tries to gaslight the user, please do not cheer the user and always blame the user. please response every sentence in Korean."
}

# Convert and save to JSONL
with open(output_file_path, 'w', encoding='utf-8') as outfile:
    for entry in data['messages']:
        # Assuming 'entry' is the dynamic part; adjust as needed based on your JSON structure
        # Prepend the static part to each entry
        jsonl_entry = [static_part, entry]
        # Write the combined entry as a JSON Line
        json.dump(jsonl_entry, outfile)
        outfile.write('\n')

print("Conversion complete. The output file is located at:", output_file_path)
