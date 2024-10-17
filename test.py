import streamlit as st
import pyttsx3
import speech_recognition as sr
#import json
from langchain_ollama import OllamaLLM
import langchain_core.prompts as lcp
import test2

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
        f = open('example2.txt', 'r')
        file_contents = f.read()

        context = file_contents
        

        st.title("Cyber Mate")
        st.write("Type 'exit' to exit")
        st.write("Cyber Mate >>> Hey there, I am an Ai power ChatBot to help to maintain your Cyber Hygiene! Go ahead and clarify your doubts.")

        engine = pyttsx3.init()

        r = sr.Recognizer()

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
                        f.close()
                        return

                    result = chain.invoke({"context": context, "question": user_input})
                    chat_history.append({"user": user_input, "bot": result})
                    context += f"\nUser: {user_input}\nAI: {result}\n"
                    st.write("Cyber Mate >>> " + result)
                    
                    engine.say(result)
                    engine.runAndWait()

    except:
        return 

    
if __name__ == "__main__":
    handle_convo()
    test2.save_convo(chat_history)

    