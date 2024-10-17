import streamlit as st
import pyttsx3
import speech_recognition as sr
import datetime
import os
from langchain_ollama import OllamaLLM
import langchain_core.prompts as lcp

template = """
Answer the question below

Here is the conversation history: {context}

Question: {question}

Answer:
"""

model = OllamaLLM(model="llama3.1")
prompt = lcp.ChatPromptTemplate.from_template(template)
chain = prompt | model
chat_history = []

def handle_convo():
    try:
        if 'conversation_file' not in st.session_state:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            conversation_file = f"conversation_{timestamp}.txt"
            st.session_state.conversation_file = open(conversation_file, 'w')

        st.write("Type 'exit' to exit")
        st.write("Cyber Mate >>> Hey there, I am an Ai power ChatBot to help to maintain your Cyber Hygiene! Go ahead and clarify your doubts.")

        engine = pyttsx3.init()

        r = sr.Recognizer()

        context = ""

        with st.form("chat_form"):
            user_input_method = st.selectbox("Select input method", ["Text", "Voice"])
            if user_input_method == "Text":
                user_input = st.text_input("User >>")
            else:
                with sr.Microphone() as source:
                    st.write("Speak now...")
                    audio = r.listen(source)
                    try:
                        user_input = r.recognize_google(audio)
                        st.write("You said: " + user_input)
                    except sr.UnknownValueError:
                        st.write("Sorry, I didn't understand that.")
                    except sr.RequestError as e:
                        st.write("Error; {0}".format(e))

            submitted = st.form_submit_button("Submit")

            if submitted:
                if user_input:
                    if user_input.lower() == "exit":
                        st.session_state.conversation_file.close()
                        return

                    result = chain.invoke({"context": context, "question": user_input})
                    chat_history.append({"user": user_input, "bot": result})
                    context += f"\nUser: {user_input}\nAI: {result}\n"
                    st.session_state.conversation_file.write(f"User: {user_input}\nAI: {result}\n\n")
                    st.write("Cyber Mate >>> " + result)

                    engine.say(result)
                    engine.runAndWait()

    except:
        return 

def display_conversations():
    folder_path = r"C:/Users/Lenovo/Desktop/evotech"
    txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    selected_file = st.selectbox("Select a conversation", txt_files)

    with open(os.path.join(folder_path, selected_file), "r") as f:
        file_contents = f.read()

    st.write(file_contents)

if __name__ == "__main__":
    st.title("Cyber Mate")
    st.write("Select an option:")
    option = st.selectbox("Options", ["Chat", "View Conversations"])

    if option == "Chat":
        handle_convo()
    else:
        display_conversations()