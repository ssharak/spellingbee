import random
from gtts import gTTS
import os
import tkinter as tk
from tkinter import messagebox

# Initialize a list to keep track of used words
used_words = []

from gtts import gTTS
from io import BytesIO
import pygame

# Initialize the text-to-speech engine
pygame.mixer.init()

def play_audio():
    selected_file = grade_choice.get()
    if selected_file == 'All':
        selected_file = 'All.txt'
    else:
        selected_file = f"{selected_file}.txt"

    global word_list

    with open(selected_file, "r") as file:
        word_list = [line.strip() for line in file]
        random.shuffle(word_list)

    # Shuffle the word list if all words have been used at least once
    if len(used_words) == len(word_list):
        used_words.clear()  # Reset the used words list

    # Select a word from the shuffled list that hasn't been used before
    global word
    word = None
    for w in word_list:
        if w not in used_words:
            word = w
            used_words.append(word)
            break

    tts_audio = gTTS(text=word, lang='en')
    audio_stream = BytesIO()
    tts_audio.write_to_fp(audio_stream)

    # Use pygame to play the audio directly from the BytesIO object
    audio_stream.seek(0)  # Reset the stream position to the beginning
    pygame.mixer.music.load(audio_stream)
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def checkword():

    global word

    global word_list

    user_input = entry.get().strip()

    if word is None:
        print('Error! Word variable is None! Contact the author for troubleshooting.')
    if user_input == word:
        # Change the background color to green for a brief moment
        entry.configure({"background": "green"})
        root.after(100, lambda: entry.configure({"background": "white"}))
    else:
        messagebox.showinfo("Result", f"Incorrect. The correct spelling is: {word}")
        used_words.remove(word)  # Remove the incorrect word from used_words
    entry.delete(0, 'end')  # Clear the entry field

# Function to check spelling or play audio depending on the entry field's content
def check_or_play_audio():
    if entry.get().strip():  # Check if the entry field is not empty
        checkword()
    else:
        play_audio()

# Create the main window
root = tk.Tk()
root.title("Spelling Bee Game")

# List all the text files in the directory with numeric names
text_files = [filename for filename in os.listdir() if (filename[:-4].isdigit() or filename == 'All.txt') and filename.endswith(".txt")]
all_txt_exists = 'All.txt' in text_files

if not text_files:
    messagebox.showinfo("Error", "No grade level spelling word files found in this directory, i.e. 3.txt, 4.txt, etc. or All.txt\n\nAdd them and restart the game.")
    root.quit()
    # If no text files are found, set the grade_choice to 'None Found'
    grade_choice = tk.StringVar(value="None Found")
else:
    # Otherwise, create the grade_choice variable and populate the dropdown menu
    grade_choice = tk.StringVar(value="All" if all_txt_exists else text_files[0][:-4])

# Create a label and dropdown for grade selection
label = tk.Label(root, text="Choose a grade level:")
label.pack()

if not all_txt_exists and text_files:
    grade_dropdown = tk.OptionMenu(root, grade_choice, *sorted(set(filename[:-4] for filename in text_files)))
elif text_files:
    grade_dropdown = tk.OptionMenu(root, grade_choice, *sorted(set(filename[:-4] for filename in text_files) | {"All"}))
else:
    grade_dropdown = tk.OptionMenu(root, grade_choice, "None Found")
    
grade_dropdown.pack()

# Create a button to start the game
start_button = tk.Button(root, text="Speak New Word\n(Or press 'Enter')", command=play_audio)
start_button.pack()

# Function to clear used_words when the grade level is changed
def clear_used_words():
    used_words.clear()

# Bind the clear_used_words function to the grade_choice variable
grade_choice.trace("w", lambda *args: clear_used_words())

# Create a text entry for spelling
entry_label = tk.Label(root, text="Spell the word you heard:")
entry_label.pack()

entry = tk.Entry(root)
entry.pack()
entry.focus()  # Set focus on the entry field

# Create a button to check the word
check_button = tk.Button(root, text="Check spelling", command=checkword)
check_button.pack()

# Bind the Enter key to the entry field to trigger the check_or_play_audio function
entry.bind("<Return>", lambda event: check_or_play_audio())

# Run the GUI main loop
root.mainloop()
