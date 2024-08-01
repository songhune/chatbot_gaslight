import os
import json
from datetime import datetime
from scenario_handler import ScenarioHandler

def chatbot_response(response, client, n=1):
    if not response:
        return "응답이 없습니다.", []

    # Initialize ScenarioHandler
    scenario_handler = ScenarioHandler()

    # Initialize messages with system message
    messages = [{"role": "system", "content": "You are a chatbot."}]
    
    # Get scenario-specific messages
    scenario_messages = scenario_handler.get_response(response.strip())
    
    if scenario_messages:
        messages.extend(scenario_messages)
    else:
        # Add user's message to history
        messages.append({"role": "user", "content": response})

    # Generate the assistant's response
    api_response = client.chat.completions.create(
        model="gpt-4",
        temperature=0.8,
        top_p=0.9,
        max_tokens=300,
        n=n,  # Generate n completions
        frequency_penalty=0.5,
        presence_penalty=0.5,
        messages=messages
    )

    # Get the assistant's response texts
    choices = [choice.message.content for choice in api_response.choices]
    # Check if the user wants to end the session
    if response.strip().lower() == "종료":
        save_history(messages)  # Save the history if the keyword "종료" is detected
        return "세션을 저장하고 종료합니다.", []

    # Return the assistant's response choices
    return messages[-1]['content'], choices

def save_history(history):
    # Generate a timestamped filename for the JSON file
    os.makedirs('logs', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join('logs', f'chat_history_{timestamp}.json')

    # Save session history to a JSON file
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(history, file, ensure_ascii=False, indent=4)
    print(f"History saved to {filename}")
