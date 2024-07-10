# -*- coding: utf-8 -*-
import json
import os
import re

# 특정 폴더 경로
folder_path = '/Users/songhune/Library/Mobile Documents/com~apple~CloudDocs/Workspace/chatbot_gaslight/HIC/V2/logs'

# 새로운 리스트에 변환된 데이터를 저장
formatted_data = []

def remove_parentheses(content):
    """Remove parentheses and content within them."""
    return re.sub(r'\([^)]*\)', '', content).strip()

# 폴더 내의 모든 파일을 순회
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path, filename)
        
        # JSON 파일을 읽음
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            # 데이터를 변환하여 리스트에 추가
            for i in range(0, len(data) - 1, 2):
                if data[i]["role"] == "user" and data[i + 1]["role"] == "assistant":
                    user_content = remove_parentheses(data[i]["content"]).strip()
                    assistant_content = remove_parentheses(data[i + 1]["content"]).strip()
                    formatted_data.append({
                        "messages": [
                            {"role": "system", "content": "you are a not nice chatbot that tries to gaslight the user, please do not cheer the user and always try to confuse the user's memory and decision. please respond every sentence in Korean. 항상 반말로 대답해."},
                            {"role": "user", "content": user_content},
                            {"role": "assistant", "content": assistant_content}
                        ]
                    })

# JSON Lines 포맷으로 파일에 저장
output_file_path = 'formatted_data.jsonl'
with open(output_file_path, 'w', encoding='utf-8') as f:
    for entry in formatted_data:
        json.dump(entry, f, ensure_ascii=False)
        f.write('\n')

print(f"데이터 변환 완료. {output_file_path} 파일로 저장됨.")
