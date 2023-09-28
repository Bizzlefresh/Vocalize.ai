import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox
import pyttsx3
import speech_recognition as sr
import os
# import openai


root = Tk()
root.title("Vocalize")
root.geometry("900x450+100+100")
root.resizable(False, False)
root.configure(bg="#305065")

engine = pyttsx3.init()

# Options for languages
languages = ['en', 'es', 'fr']  # Add the desired languages to the list

language_var = StringVar()  # Create a variable to store the selected language
language_var.set(languages[0])  # Set the default language

Label(root, text="SELECT LANGUAGES", font="arial 15 bold", bg="#305065", fg="white").place(x=670, y=360)

language_dropdown = OptionMenu(root, language_var, *languages)  # Create the dropdown menu
language_dropdown.place(x=800, y=400)  # Display the dropdown menu

# Select language

selected_language = language_var.get()

# Set the tracking of the dark mode
dark_mode = StringVar()
dark_mode.set("Off")

# Function to translate audio through openai
# def translate_audio():
#     openai.api_key = os.getenv("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")
#     audio_file = open("captured_audio.mp3.txt", "rb")
#     transcript = openai.Audio.translate('whisper-1', audio_file, selected_language)
#     text_area.delete("1.0", tk.END)
#     text_area.insert(tk.END, transcript)


# Function to toggle the dark mode
def toggle_dark_mode():
    if dark_mode.get() == "Off":
        # Set dark mode Off
        root.configure(bg="black")
        dark_mode.set("On")

    else:
        # Set the dark mode On
        root.configure(bg="#305065")
        dark_mode.set("Off")


# Set the Voice function
def voice_detection():
    r = sr.Recognizer()
    r.energy_threshold = 4000
    with sr.Microphone() as source:
        text = "Listening"
        print(text)
        # text_area.delete("1.0", tk.END)
        # text_area.insert(tk.END, text)
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        # engine.save_to_file(audio, 'captured_audio.mp3.txt')

    # try:
    #     if selected_language == "yo":
    #         translate_audio()
    #     else:
    #         text = r.recognize_google(audio, language=selected_language)
    #         text_area.delete("1.0", tk.END)
    #         text_area.insert(tk.END, text)

    try:
        text_area.delete("1.0", tk.END)
        text = r.recognize_google(audio, language=selected_language)
        text_area.insert(tk.END, text)

    except sr.UnknownValueError:
        text_area.delete("1.0", tk.END)
        text = "Sorry, I couldn't understand."
        text_area.insert(tk.END, text)

    except sr.RequestError:
        text_area.delete("1.0", tk.END)
        text = "Sorry, I'm having trouble accessing the speech recognition service."
        text_area.insert(tk.END, text)


# Voice and Save Function
def speaknow():
    text = text_area.get(1.0, END)
    gender = gender_combobox.get()
    speed = speed_combobox.get()
    voices = engine.getProperty('voices')

    def setvoice():
        if gender == 'Male':
            selected_language = language_var.get()
            engine.setProperty('voice', voices[0].id)
            engine.setProperty('language', selected_language)
            engine.say(text)
            engine.runAndWait()

        else:
            selected_language = language_var.get()
            engine.setProperty('voice', voices[1].id)
            engine.setProperty('language', selected_language)
            engine.say(text)
            engine.runAndWait()

    if text:
        if speed == "Fast":
            engine.setProperty('rate', 250)
            setvoice()

        elif speed == "Normal":
            engine.setProperty('rate', 150)
            setvoice()

        else:
            engine.setProperty('rate', 60)
            setvoice()

    voice_detection()


def download():
    text = text_area.get(1.0, END)
    gender = gender_combobox.get()
    speed = speed_combobox.get()
    voices = engine.getProperty('voices')

    def setvoice():
        if gender == 'Male':
            engine.setProperty('voice', voices[0].id)
            path = filedialog.askdirectory()
            os.chdir(path)
            engine.save_to_file(text, 'text.mp3')
            engine.runAndWait()

        else:
            engine.setProperty('voice', voices[1].id)
            path = filedialog.askdirectory()
            os.chdir(path)
            engine.save_to_file(text, 'text.mp3')
            engine.runAndWait()

    if text:
        if speed == "Fast":
            engine.setProperty('rate', 250)
            setvoice()

        elif speed == "Normal":
            engine.setProperty('rate', 150)
            setvoice()

        else:
            engine.setProperty('rate', 60)
            setvoice()

    voice_detection()


# icon


image_icon = PhotoImage(file="Text2Speech.png")
root.iconphoto(False, image_icon)

# Top Frame


Top_frame = Frame(root, bg="white", width=900, height=100)
Top_frame.place(x=0, y=0)

Logo = PhotoImage(file="vocalize_ai.png")
Label(Top_frame, image=Logo, bg="white").place(x=10, y=5)
Label(Top_frame, text="Vocalize: Speak Your Mind", font="Helvetica 20 bold", bg="white", fg="#352F44").place(x=300,
                                                                                                             y=30)
image_icon3 = PhotoImage(file="moon2.png")
dark_mode_button = Button(Top_frame, compound=RIGHT, image=image_icon3, width=89, height=30, command=toggle_dark_mode)
dark_mode_button.place(x=800, y=30)

# Below Frame
text_area = Text(root, font="Robote 16", bg="#498A92", fg="#E1FFFD", relief=GROOVE, wrap=WORD)
text_area.place(x=10, y=150, width=500, height=250)

Label(root, text="VOICE", font="arial 15 bold", bg="#305065", fg="white").place(x=580, y=160)
Label(root, text="SPEED", font="arial 15 bold", bg="#305065", fg="white").place(x=760, y=160)

gender_combobox = Combobox(root, values=['Male', 'Female'], font="arial 10", state='r', width=10)
gender_combobox.place(x=550, y=200)
gender_combobox.set('Male')

speed_combobox = Combobox(root, values=['Fast', 'Normal', 'Slow'], font="arial 10", state='r', width=10)
speed_combobox.place(x=730, y=200)
speed_combobox.set('Normal')

image_icon = PhotoImage(file="Mic.png")
speak = Button(root, text="Speak", compound=LEFT, image=image_icon, width=130, font="arial 14 bold", command=speaknow)
speak.place(x=550, y=280)

image_icon2 = PhotoImage(file="download.png")
save = Button(root, text="Save", compound=LEFT, image=image_icon2, width=130, bg="#39c790", font="arial 14 bold",
              command=download)
save.place(x=730, y=280)

root.mainloop()
