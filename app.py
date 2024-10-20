import streamlit as st
import pandas as pd
import re
import uuid
import subprocess
import os 
import json

from dotenv import load_dotenv
from curl_response import get_chat_completion
# Load environment variables from .env file
load_dotenv()
# Title of the web app
st.title("PLOT GPT")
model_name = "llama3-8b-8192"
model_name = 'llama-3.2-1b-preview'

# Upload CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_KEY2 = os.getenv("GROQ_API_KEY2")

# Radio button for training data generation vs inference
mode = st.radio("Select mode:", ("Training Data Generation", "Inference"))

def extract_code_blocks(text):
    print("line 25 text", type(text), text)
    # breakpoint()
    text = text.replace("Python", "")
    text = text.replace("python", "")
    # Regular expression pattern to find code blocks surrounded by triple backticks
    pattern = r"'''(.*)"
    pattern2 = r"(.*)'''"
    pattern_sub_1 =  r"```(.*)"
    pattern_sub_2 = r"(.*)```"
    # Using re.DOTALL to make the dot match newlines as well
    matches = re.findall(pattern, text, re.DOTALL)
    if not matches:
        matches = re.findall(pattern_sub_1, text, re.DOTALL)

        matches2 = re.findall(pattern_sub_2, matches[0], re.DOTALL)
    else:
        matches2 = re.findall(pattern2, matches[0], re.DOTALL)
    # 'matches' will be a list of all the code blocks found in the text
    return matches2

def create_python_file(response):
    global model_name
    code_blocks = extract_code_blocks(response)
    csv_file_path = "user_behavior_dataset.csv"
    filename = f"plot_{uuid.uuid4().hex[:8]}"
    if code_blocks:
        for block in code_blocks:
            print("Found code block:")
            print(block.strip())
            code_block = block.strip()
            code_block_temp = code_block
            code_block = code_block.replace("dataset.csv", csv_file_path)
            
            # Append code_block to save the plot
            png_file_path = os.path.join("png_files", f"{filename}.png")
            code_block += f"\nplt.savefig('{png_file_path}')" 
    
    if code_block is not None:
        # Open the file in write mode ('w') which will overwrite the file if it already exists
        file_path = os.path.join("code_files", f"{filename}.py")
        with open(file_path, 'w') as file:
            file.write(code_block)
    else:
        print("No code block found in the response.")
    return file_path, code_block_temp

def groq_call(user_input, df):
    global model_name
    client = Groq(api_key=GROQ_API_KEY)
    prompt =f" A dataset contains these columns: {df.columns.tolist()} \
                    python code to do the following : {user_input}. Tips: Use matplotlib library to create the plot and assume I already have the library installed. \
                    only givem me the code else I will kill someone if you give extra information or anything else. \
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
        # model="llama3-b-8192",
        model=model_name
    )
    text = chat_completion.choices[0].message.content
    return text, prompt

def main():
    global model_name
    total_plots = 0
    correct_plots = 0
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into a pandas DataFrame
        df = pd.read_csv(uploaded_file)
        user_input = st.text_input("Prompt :")

        if mode == "Training Data Generation":
            user_input_gpt = [
                "Histogram of App Usage Time (min/day)",
                "Bar Plot of Average App Usage Time by Device Model",
                "Scatter Plot of Screen On Time vs. Battery Drain",
                "Bar Plot of Number of Apps Installed by Operating System",
                "Box Plot of Screen On Time by Gender",
                "Correlation Heatmap of Numeric Features (App Usage, Screen On Time, Battery Drain, Data Usage, etc.)",
                "Bar Plot of Average Data Usage by Age",
                "Pie Chart of Device Model Distribution",
                "Bar Plot of Average Battery Drain by User Behavior Class",
                "Scatter Plot of Age vs. Screen On Time",
                "Box Plot of Data Usage by Gender",
                "Line Plot of Average App Usage Time by Age Group",
                "Stacked Bar Plot of User Behavior Class by Operating System",
                "Bar Plot of Average Screen On Time by Device Model",
                "Density Plot of Battery Drain by Gender"
            ]
            # Display the dataframe
            st.write("Columns in the dataset:")
            st.write("Here is a preview of the dataset:")
            st.write(df.head())
            # Display the columns in the dataset
            st.write(df.columns.tolist())
            for user_input in user_input_gpt:
                # text, prompt = groq_call(user_input, df)
                text,prompt = get_chat_completion(user_input, df)
                try:
                    file_path, code_temp = create_python_file(text)
                    skip = False
                    command = f"python {file_path}"
                    train_data = {"instruction": prompt,"input": "","output": code_temp}
                    base_path = os.path.basename(file_path)[:-3]
                    train_data_path = os.path.join("train_data", f"train_data_{base_path}.json")
                    if not os.path.exists("train_data"):
                        os.makedirs("train_data", exist_ok=True)
                    with open(train_data_path, 'w') as f:
                        json.dump(train_data, f)
                except:
                    skip = True
                    file_path = "None"
                    command = ""
                    train_data_path = ""
                if file_path:
                    result = subprocess.run(command, shell=True)
                    total_plots += 1
                    if result.returncode == 0 and not skip:
                        st.image(os.path.join("png_files",f"{base_path}.png"))
                        correct_plots += 1
                    else:
                        st.write("Error in running the code. Please try again.")
                        
                        if os.path.exists(file_path):  # Check if the file exists
                            os.remove(file_path)  # Remove the file if there is an error
                        if os.path.exists(train_data_path):
                            os.remove(train_data_path) # remove the train data if there is an error
                else:
                    st.write("No valid code block found to run.")
                
                # Display summary statistics
                st.write("Summary Statistics:")
                st.write(df.describe())
            st.write(f"Correct plots: {correct_plots}, Total plots: {total_plots}, Accuracy: {correct_plots*100/total_plots}%")
                    # Write correct plot accuracy and total plots to another json file called accuracy.json
            accuracy = {
                "csv_file_name": uploaded_file.name,       # Add the CSV file name
                "correct_plots": correct_plots,
                "total_plots": total_plots,
                "accuracy": correct_plots / total_plots,
                "questions_list": user_input_gpt,  # Add the questions list
                "groq_model": model_name
            }
            with open("accuracy.json", "a") as f:
                json.dump(accuracy, f)
                f.write("\n")  # Ensure each entry is on a new line
        
        else:  # Inference mode

            if user_input:
                st.write("Here is a preview of the dataset:")
                st.write(df.head())

                # Display the columns in the dataset
                st.write("Columns in the dataset:")
                st.write(df.columns.tolist())
                # text, prompt = groq_call(user_input, df)
                text, prompt = get_chat_completion(user_input, df)
                file_path, code_temp = create_python_file(text)
                base_path = os.path.basename(file_path)[:-3]

                command = f"python {file_path}"
                if file_path:
                    result = subprocess.run(command, shell=True)
                    total_plots += 1
                    if result.returncode == 0:
                        st.image(os.path.join("png_files",f"{base_path}.png"))
                        correct_plots += 1
                    else:
                        st.write("Error in running the code. Please try again.")
                        os.remove(file_path) # remove the file if there is an error
                else:
                    st.write("No valid code block found to run.")
                
                # Display summary statistics
                st.write("Summary Statistics:")
                st.write(df.describe())
        


if __name__ == "__main__":
    main()
