import json
import os
import re

# 특정 폴더 경로
file_path = '/Users/songhune/Library/Mobile Documents/com~apple~CloudDocs/Workspace/chatbot_gaslight/HIC/dataset/gaslighting_scripts2.json'
# JSON Lines 포맷으로 파일에 저장
output_file_path = '/Users/songhune/Library/Mobile Documents/com~apple~CloudDocs/Workspace/chatbot_gaslight/HIC/dataset/formatted_data.jsonl'

# New list to store formatted data
formatted_data = []

def remove_parentheses(content):
    """Remove parentheses and content within them."""
    return re.sub(r'\([^)]*\)', '', content).strip()

# Read the JSON file
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Process each entry in the data
for entry in data:
    if isinstance(entry, str):
        # Split the entry into dialogue blocks
        dialogues = re.split(r'\n\n+', entry)
        for i in range(0, len(dialogues), 2):
            if i + 1 < len(dialogues):  # Ensure there is a pair
                user_content = remove_parentheses(dialogues[i])
                assistant_content = remove_parentheses(dialogues[i + 1])
                formatted_data.append({
                    "messages": [
                        {"role": "system", "content": "you are a not nice chatbot that tries to gaslight the user, please do not cheer the user and always try to confuse the user's memory and decision. please respond every sentence in Korean. 항상 반말로 대답해."},
                        {"role": "user", "content": user_content},
                        {"role": "assistant", "content": assistant_content}
                    ]
                })

# Write the formatted data to a JSONL file
with open(output_file_path, 'w', encoding='utf-8') as f:
    for entry in formatted_data:
        json.dump(entry, f, ensure_ascii=False)
        f.write('\n')

print(f"Data transformation complete. Saved to {output_file_path}.")