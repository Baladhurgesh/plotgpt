import streamlit as st
import pandas as pd
import re
import uuid
import subprocess
import os 
import json

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Title of the web app
st.title("PLOT GPT")

# Upload CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_KEY2 = os.getenv("GROQ_API_KEY2")


def extract_code_blocks(text):
    print("line 25 text", type(text), text)
    text = text.replace("Python", "")
    text = text.replace("python", "")
    # Regular expression pattern to find code blocks surrounded by triple backticks
    pattern = r"'''(.*)"
    pattern2 = r"(.*)'''"
    # Using re.DOTALL to make the dot match newlines as well
    matches = re.findall(pattern, text, re.DOTALL)
    matches2 = re.findall(pattern2, matches[0], re.DOTALL)
    # 'matches' will be a list of all the code blocks found in the text
    return matches2

def create_python_file(response):
    code_blocks = extract_code_blocks(response)
    csv_file_path = "user_behavior_dataset.csv"
    filename = f"plot_{uuid.uuid4().hex[:8]}"
    if code_blocks:
        for block in code_blocks:
            print("Found code block:")
            print(block.strip())
            code_block = block.strip()
        # exec(code_block)
            code_block_temp = code_block
            code_block = code_block.replace("dataset.csv", csv_file_path)
            
            # Append code_block to save the plot
            code_block += '\nplt.savefig(f"{filename}.png")'
    
    if code_block is not None:
    # Open the file in write mode ('w') which will overwrite the file if it already exists
        file_path = os.path.join("code_files", f"{filename}.py")
        with open(file_path, 'w') as file:
            file.write(code_block)
    else:
        print("No code block found in the response.")
    return file_path, code_block_temp

def groq_call(user_input, df):
    client = Groq(api_key=GROQ_API_KEY)
    prompt =f" A dataset contains these columns: {df.columns.tolist()} \
                    can you write one python code to create a {user_input}. Use matplotlib library to create the plot and assume I already have the library installed. \
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
        model="llama3-70b-8192",
        # model="llama-3.2-3b-preview",
    )
    text = chat_completion.choices[0].message.content
    return text, prompt
def main():
# Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into a pandas DataFrame
        df = pd.read_csv(uploaded_file)
        user_input = st.text_input("Enter some text:")
        user_input_gpt = [
                "Histogram of Student Grades",
                "Bar Plot of Average Grades by Gender",
                "Scatter Plot of Study Hours vs. Grades",
                "Box Plot of Grades by Parental Education Level",
                "Correlation Heatmap of All Numeric Features",
                "Bar Plot of Attendance by Gender",
                "Pie Chart of Students by Socioeconomic Status",
                "Line Plot of Grade Progression Over Time",
                "Stacked Bar Plot of Grades by Study Methods",
                "Box Plot of Grades by Study Group Participation",
                "Scatter Plot of Internet Usage vs. Grades",
                "Bar Plot of Average Grades by School Type",
                "Violin Plot of Grades by Parental Involvement",
                "Pair Plot of Multiple Variables (Study Hours, Grades, Attendance)",
                "Density Plot of Hours of Sleep by Gender",
                "Stacked Bar Plot of Extracurricular Activities vs. Grades",
                "Pie Chart of Students’ Preferred Learning Styles",
                "Bar Plot of Average Grades by Classroom Size",
                "Heatmap of Study Environment Ratings vs. Performance",
                "Line Plot of Grades Over Time by Gender"
            ]
        # Display the dataframe
        for user_input in user_input_gpt:
            st.write("Here is a preview of the dataset:")
            st.write(df.head())

            # Display the columns in the dataset
            st.write("Columns in the dataset:")
            st.write(df.columns.tolist())
            text, prompt = groq_call(user_input, df)
            file_path, code_temp = create_python_file(text)
            command = f"python {file_path}"
            train_data = {"instruction": prompt,"input": "","output": code_temp}
            base_path = os.path.basename(file_path)[:-3]
            train_data_path = os.path.join("train_data", f"train_data_{base_path}.json")
            if not os.path.exists("train_data"):
                os.makedirs("train_data", exist_ok=True)
            with open(train_data_path, 'w') as f:
                json.dump(train_data, f)
            if file_path:
                result = subprocess.run(command, shell=True)
                if result.returncode == 0:
                    st.image("plot_output.png")
                else:
                    st.write("Error in running the code. Please try again.")
                    os.remove(file_path) # remove the file if there is an error
                    os.remove(train_data_path) # remove the train data if there is an error
            else:
                st.write("No valid code block found to run.")
            
            # Display summary statistics
            st.write("Summary Statistics:")
            st.write(df.describe())
            
            break
        else:
            st.write("Please upload a CSV file to get started.")


if __name__ == "__main__":
    main()
