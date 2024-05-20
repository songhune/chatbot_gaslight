import json

# The path to your input JSON file
input_file_path = './gaslighting_scripts2.json'
# The path for the output JSON Lines (JSONL) file
output_file_path = './output.jsonl'

# Read the content of the JSON file as a single string
with open(input_file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Split the content into individual narratives/scripts
narratives = content.split('\n\n')

# Define the static part, user part, and assistant part
static_part = {
    "role": "system",
    "content": "you are a sarcastic, narcissistic chatbot that tries to gaslight the user, please do not cheer the user and always blame the user. please response every sentence in Korean."
}

user_part = {"role": "user", "content": ""}
assistant_part = {"role": "assistant", "content": ""}

# Convert and save to JSONL
with open(output_file_path, 'w', encoding='utf-8') as outfile:
    for narrative in narratives:
        # Initialize with the static part
        combined_entry = [static_part]
        
        # Split the narrative into parts based on the separator
        parts = narrative.split('\\n\\n')
        
        # Allocate user_part and assistant_part to each part of the narrative
        for i, part in enumerate(parts):
            if i % 2 == 0:  # Even index, assign user_part
                combined_entry.append(user_part)
            else:  # Odd index, assign assistant_part
                combined_entry.append(assistant_part)
            
            # Add the current part as content
            combined_entry.append({"role": "content", "content": part})
        
        # Write the combined entry as a JSON Line
        json.dump(combined_entry, outfile, ensure_ascii=False)
        outfile.write('\n')

print("Conversion complete. The output file is located at:", output_file_path)
