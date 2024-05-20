# Gaslighting Chatbot

## Description
가스라이팅 챗봇 프로젝트

## Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

## Setup Instructions

1. Clone the repository:
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. Create a virtual environment (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the project root directory and add your OpenAI API key:
    ```plaintext
    OPENAI_API_KEY=sk-YourOpenAIKeyHere
    ```
    별도의 openai api를 필요로 합니다.

5. Add `.env` to `.gitignore` to ensure it is not tracked by git:
    ```plaintext
    # .gitignore
    .env
    ```

6. Run the chatbot:
    HIC폴더 내부의 V1~Vx까지 가능

## File Descriptions

- `chatbot.py`: The main script to run the chatbot.
- `requirements.txt`: Lists the dependencies required for the project.
- `.env`: File to store environment variables (e.g., API keys). **Do not commit this file to version control.**
- `.gitignore`: Ensures `.env` and other files are not tracked by git.
- `README.md`: This readme file.
