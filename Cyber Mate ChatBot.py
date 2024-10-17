import streamlit as st #for web app UI
import pyttsx3 #for text to speech
import speech_recognition as sr #for voice input
import os, json, datetime #datetime for conversation history timestamp
import langchain.globals as langchain_globals #longchain global since we did not use environment
from langchain_ollama import OllamaLLM #using the OllamaLLM
import langchain_core.prompts as lcp #for prompt formatting

langchain_globals.set_verbose(True)  #speeds up the code and output from model is formatted

#template for the model is definded 
template = """
Answer the question below

Here is the conversation history: {context}

Question: {question}

Answer:
"""

model = OllamaLLM(model="llama3.1") #model is initialized
prompt = lcp.ChatPromptTemplate.from_template(template) #promt template for the model is defined 
chain = prompt | model #chain of action is defined 
chat_history = [] #used to store the chat history

def get_voice_input():
    r = sr.Recognizer() #initializes the voice input controller
    with sr.Microphone() as source: #checks for microphonephone
        print("Speak now...")
        audio = r.listen(source) #takes in the audio
        try:
            user_input = r.recognize_google(audio) #audio is converted to text using google speech to text
            print("You said: " + user_input)
            return user_input
        except sr.UnknownValueError: #error handled if input is not converted to text succesfully
            print("Sorry, I didn't understand that.")
            return ""
        except sr.RequestError as e: #If we are unable to connect to the server of google
            print("Error; {0}".format(e))
            return ""

def handle_convo():
    try:
        if 'conversation_file' not in st.session_state:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")#gets the timestamp
            conversation_file = fr"C:/Users/Lenovo/Desktop/evotech/prev_conversation/conversation__{timestamp}.txt" #the conversation file is created
            st.session_state.conversation_file = open(conversation_file, 'w') #opens a file in session varibale
            st.session_state.conversation_file.write("Cyber Mate >>> Hey there, I am an Ai power ChatBot to help to maintain your Cyber Hygiene! Go ahead and clarify your doubts.\n\n")

        st.title("Cyber Mate")
        st.write("Type 'exit' to exit")
        st.write("Cyber Mate >>> Hey there, I am an Ai power ChatBot to help to maintain your Cyber Hygiene! Go ahead and clarify your doubts.")

        engine = pyttsx3.init() #initializes the voice output engine

        f = open(r'C:/Users/Lenovo/Desktop/evotech/database/example2.txt', 'r')
        file_contents = f.read()

        context = file_contents #give the bot some data so it knows what it is
        
        user_input_method = st.selectbox("Select input method", ["Text", "Voice"]) #dropdown menu to select input method
        if user_input_method == "Text":
            user_input = st.text_input("User >>") #takes input from user
        else:
            user_input = "" #clears the user input
            voice_button = st.button("Click to speak") #button to start speaking
            if voice_button:
                user_input = get_voice_input() #takes in the voice input
                st.session_state.voice_input = user_input #input is transferred to session variable
                st.write("You said: " + user_input) #displays the voice input

        submitted = st.button("Submit")

        if submitted:
            if 'voice_input' in st.session_state: #check if the selected input form is voice
                user_input = st.session_state.voice_input #the voice input is parsed as uber input
            if user_input: #code for exitting the program
                if user_input.lower() == "exit":
                    user_input = ""
                    st.session_state.conversation_file.close()
                    st.stop() #stops the session
                    return

                result = chain.invoke({"context": context, "question": user_input}) #invokes answer
                chat_history.append({"user": user_input, "bot": result}) #chat conversation with bot is added to the list 
                context += f"\nUser: {user_input}\nAI: {result}\n" #provides the context, such that previous conversation is also in knowledge of the bot
                st.session_state.conversation_file.write(f"User: {user_input}\nAI: {result}\n\n") #saves the conversation hisotry to the file
                st.session_state.conversation_file.flush()  #the buffer variables are flushed, fasts the running speed also
                st.write("Cyber Mate >>> " + result) #output is displayed

                engine.say(result) #output is spoken out
                engine.runAndWait()

    except:
        return 

if __name__ == "__main__":
    handle_convo() #the function is called