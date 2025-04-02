import tkinter as tk
from tkinter import messagebox
import pyttsx3
import speech_recognition as sr
import random
import webbrowser
import datetime
import pyautogui
import wikipedia
import pywhatkit as pwk
import mtranslate
import openai
import requests
from PIL import Image
import io
import pyaudio

# Ava voice setup
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Set voice to a specific index
engine.setProperty("rate", 150)

# OpenAI API setup
openai_key = "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"

# Replace with your OpenAI API key

# Speak Function
def speak(audio):
    audio = mtranslate.translate(audio, to_language="en", from_language="en-in")
    print(audio)
    engine.say(audio)
    engine.runAndWait()

# Recognize Speech Function
def command():
    content = " "
    while content == " ":
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)

        try:
            content = r.recognize_google(audio, language='en-in')
            print("You Said....." + content)
            content = mtranslate.translate(content, to_language="en-in")
            print("You Said....." + content)
        except Exception as e:
            print("Please try again...")
    return content

# Function to send AI request
def send_request(query):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=query
    )
    return response.choices[0].message['content']

# Function to generate image
def generate_image(prompt):
    response = openai.Image.create(
        model="dall-e-2",
        prompt=prompt,
        n=1,
        size="1024x1024",
        quality="standard"
    )

    image_url = response['data'][0]['url']
    data = requests.get(image_url).content

    with open("img.jpg", "wb") as f:
        f.write(data)

    img = Image.open(io.BytesIO(data))
    img.show()
    webbrowser.open(image_url)

# Main process handling commands
def main_process_GUI(request):
    if "hello" in request:
        return "Welcome! How can I help you?"
    
    elif "play music" in request:
        song = random.randint(1, 3)
        if song == 1:
            webbrowser.open("https://www.youtube.com/watch?v=21c1OOu_53E")
        elif song == 2:
            webbrowser.open("https://www.youtube.com/watch?v=aMl4QPINI1U&list=RDMM&start_radio=1&rv=21c1OOu_53E")
        elif song == 3:
            webbrowser.open("https://www.youtube.com/watch?v=PL8X5gq9ZlQ&list=RDMM&index=2")
        return "Playing music..."
    
    elif "say time" in request:
        now_time = datetime.datetime.now().strftime("%H:%M")
        return f"The current time is {now_time}"
    
    elif "say date" in request:
        now_date = datetime.datetime.now().strftime("%d:%m:%Y")
        return f"Today's date is {now_date}"
    
    elif "new task" in request:
        task = request.replace("new task", "").strip()
        if task:
            with open("todo.txt", "a") as file:
                file.write(task + "\n")
            return f"Added task: {task}"
        
    elif "speak task" in request:
        try:
            with open("todo.txt", "r") as file:
                tasks = file.read()
            return f"Your tasks are: {tasks}"
        except FileNotFoundError:
            return "No tasks found."
        
    elif "open youtube" in request:
        webbrowser.open("www.youtube.com")
        return "Opening YouTube"
    
    elif "open" in request:
        query = request.replace("open", "").strip()
        pyautogui.press("super")
        pyautogui.typewrite(query)
        pyautogui.sleep(2)
        pyautogui.press("enter")
        return f"Opening {query}"
    
    elif "wikipedia" in request:
        query = request.replace("search wikipedia", "").strip()
        result = wikipedia.summary(query, sentences=2)
        return result
    
    elif "search google" in request:
        query = request.replace("search google", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Searching Google for {query}"
    
    elif "send whatsapp" in request:
        pwk.sendwhatmsg("+918957009525", "Hello from Ava!", 21, 53, 20)
        return "WhatsApp message sent!"
    
    elif "clear chat" in request:
        return "Chat history cleared."
    
    elif "image" in request:
        generate_image(request)
        return "Generating image..."
    
    elif "ask ai" in request:
        Ava_chat = [{"role": "user", "content": request.replace("ask ai", "").strip()}]
        response = send_request(Ava_chat)
        return response
    
    else:
        return "Sorry, I didn't understand that command."

# GUI Setup
root = tk.Tk()
root.title("Ava - Your Virtual Assistant")
root.geometry("800x500")
root.configure(bg='#121212')  # Dark background

# Custom color scheme
bg_color = '#121212'  # Dark background
fg_color = '#ffffff'  # White text
button_bg = '#333333'  # Dark gray buttons
button_fg = '#ffffff'  # White button text
entry_bg = '#333333'  # Dark gray input fields
entry_fg = '#ffffff'  # White input text
history_bg = '#1e1e1e'  # Slightly lighter dark gray for history panel
history_fg = '#ffffff'  # White history text

history = []

# Execute Command Function
def execute_command():
    try:
        request = input_box.get("1.0", tk.END).strip()
        if not request:
            messagebox.showwarning("Input Error", "Please enter a command.")
            return
        response = main_process_GUI(request)
        history.append(request)
        history_list.insert(tk.END, request)
        output_box.delete("1.0", tk.END)
        output_box.insert("1.0", f"Ava: {response}\n")
        speak(response)
        input_box.delete("1.0", tk.END)  # Clear the input box after execution
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Execute Speech Command Function
def execute_speech_command():
    try:
        request = command()
        if not request:
            messagebox.showwarning("Input Error", "Could not recognize your voice. Please try again.")
            return
        response = main_process_GUI(request)
        history.append(request)
        history_list.insert(tk.END, request)
        output_box.delete("1.0", tk.END)
        output_box.insert("1.0", f"Ava: {response}\n")
        speak(response)
        input_box.delete("1.0", tk.END)  # Clear the input box after execution
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Resize Widgets Dynamically
def resize_widgets(event):
    label.config(font=("Helvetica", 16))
    history_label.config(font=("Helvetica", 14))
    history_list.config(height=20, width=30)
    output_box.config(height=event.height // 30, width=(event.width - 200) // 10)

# GUI Components
label = tk.Label(root, text="Welcome to Ava", font=("Helvetica", 16), bg=bg_color, fg=fg_color)
label.pack(pady=10)

# Button Frame
button_frame = tk.Frame(root, bg=bg_color)
button_frame.pack(fill=tk.X, pady=5)

btn_execute = tk.Button(button_frame, text="Execute Command", command=execute_command, 
                        width=20, bg=button_bg, fg=button_fg, activebackground='#444444')
btn_execute.pack(side=tk.LEFT, padx=20)

btn_say = tk.Button(button_frame, text="Say Something", command=execute_speech_command, 
                    width=20, bg=button_bg, fg=button_fg, activebackground='#444444')
btn_say.pack(side=tk.LEFT, padx=20)

btn_exit = tk.Button(button_frame, text="Exit", command=root.quit, 
                     width=20, bg='#660000', fg=button_fg, activebackground='#880000')
btn_exit.pack(side=tk.RIGHT, padx=20)

# Main Frame
main_frame = tk.Frame(root, bg=bg_color)
main_frame.pack(fill=tk.BOTH, expand=True)

# History Frame
history_frame = tk.Frame(main_frame, bg=history_bg, width=200)
history_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

history_label = tk.Label(history_frame, text="History", font=("Helvetica", 14), 
                         bg=history_bg, fg=history_fg)
history_label.pack(anchor=tk.NW, padx=5, pady=5)

history_list = tk.Listbox(history_frame, height=20, width=30, bg=history_bg, 
                          fg=history_fg, selectbackground='#444444')
history_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Right Frame
right_frame = tk.Frame(main_frame, bg=bg_color)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Input Box (with placeholder "Message Input")
input_label = tk.Label(right_frame, text="Message Input", font=("Helvetica", 12), 
                       bg=bg_color, fg=fg_color)
input_label.pack(anchor=tk.W, padx=5, pady=5)

input_box = tk.Text(right_frame, height=5, width=60, bg=entry_bg, fg=entry_fg, 
                    insertbackground='white')
input_box.pack(fill=tk.X, padx=5, pady=5)

# Output Box (with title "Response Ava")
output_label = tk.Label(right_frame, text="Response Ava", font=("Helvetica", 12), 
                        bg=bg_color, fg=fg_color)
output_label.pack(anchor=tk.W, padx=5, pady=5)

output_box = tk.Text(right_frame, height=15, width=60, bg=entry_bg, fg=entry_fg, 
                     insertbackground='white')
output_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Run the GUI loop
root.mainloop()