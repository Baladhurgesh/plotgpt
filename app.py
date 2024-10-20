import streamlit as st
import pandas as pd
import re
import uuid
import subprocess
import os 
import json
# Title of the web app
st.title("PLOT GPT")

# Upload CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
from groq import Groq
GROQ_API_KEY = ''




def extract_code_blocks(text):
    # Regular expression pattern to find code blocks surrounded by triple backticks
    pattern = r"'''python(.*?)'''"

    # Using re.DOTALL to make the dot match newlines as well
    matches = re.findall(pattern, text, re.DOTALL)

    # 'matches' will be a list of all the code blocks found in the text
    return matches

def create_python_file(response):
    code_blocks = extract_code_blocks(response)
    csv_file_path = "/Users/bala/Downloads/user_behavior_dataset.csv"
    if code_blocks:
        for block in code_blocks:
            print("Found code block:")
            print(block.strip())
            code_block = block.strip()
        # exec(code_block)
            code_block_temp = code_block
            code_block = code_block.replace("dataset.csv", csv_file_path)
            
            # Append code_block to save the plot
            code_block += "\nplt.savefig('plot_output.png')"
    filename = f"plot_{uuid.uuid4().hex[:8]}"
    if code_block is not None:
    # Open the file in write mode ('w') which will overwrite the file if it already exists
        file_path = os.path.join("code_files", f"{filename}.py")
        with open(file_path, 'w') as file:
            file.write(code_block)
    else:
        print("No code block found in the response.")
    return file_path, code_block_temp

# Check if a file has been uploaded
if uploaded_file is not None:
    # Read the file into a pandas DataFrame
    df = pd.read_csv(uploaded_file)
    user_input = st.text_input("Enter some text:")

    # Display the dataframe
    if user_input:
        st.write("Here is a preview of the dataset:")
        st.write(df.head())

        # Display the columns in the dataset
        st.write("Columns in the dataset:")
        st.write(df.columns.tolist())
        client = Groq(api_key=GROQ_API_KEY)
        prompt =f" A dataset contains these columns: {df.columns.tolist()} \
                        can you write one python code to create a {user_input} \
                        Please write ALL the code needed since it will be extracted directly and run from your response.\
                        Always have the csv file name to be 'dataset.csv'\
                        Always start the code with '''python and end with '''"
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
        )
        text = chat_completion.choices[0].message.content
        file_path, code_temp = create_python_file(text)
        command = f"python {file_path}"
        train_data = {"instruction": prompt,"input": "","output": code_temp}
        base_path = os.path.basename(file_path)[:-3]
        train_data_path = os.path.join("train_data", f"train_data_{base_path}.json")
        with open(train_data_path, 'w') as f:
            json.dump(train_data, f)
        if file_path:
            subprocess.run(command, shell=True)
            st.image("plot_output.png")
        else:
            st.write("No valid code block found to run.")
        
        # Display summary statistics
        st.write("Summary Statistics:")
        st.write(df.describe())
        

    else:
        st.write("Please upload a CSV file to get started.")