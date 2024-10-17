import streamlit as st
import os

st.title("Previous Conversations")
# Set the folder path
folder_path = r"C:/Users/Lenovo/Desktop/evotech/prev_conversation"

# Get a list of all .txt files in the folder
txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

# Create a selectbox to choose which file to display
selected_file = st.selectbox("Select a file", txt_files)

# Read the contents of the selected file
with open(os.path.join(folder_path, selected_file), "r") as f:
    file_contents = f.read()
# Display the file contents as a page in Streamlit
st.write(file_contents)