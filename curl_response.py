import requests
import json

def get_chat_completion(user_input, df):
    url = "https://7208-195-242-23-154.ngrok-free.app/v1/chat/completions"

    headers = {
        "Content-Type": "application/json"
    }
    prompt =f" A dataset contains these columns: {df.columns.tolist()} \
                    python code to do the following : {user_input}. Tips: Use matplotlib library to create the plot and assume I already have the library installed. \
                    only givem me the code else I will kill someone if you give extra information or anything else. \
                    Please write ALL the code needed since it will be extracted directly and run from your response.\
                    Always have the csv file name to be 'dataset.csv'\
                    Always start the code with '''python and end with '''"
    
    data = {
        "model": "meta-llama/Meta-Llama-3-0.2B-Instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.1,
        "max_tokens": 1024
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content'], prompt
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return f"Error: {response.status_code}, {response.text}"
    