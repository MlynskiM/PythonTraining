# Imported modules
from tkinter import *
import random
import pandas


# --------------------------------- Variables Definition ---------------------------# 

# Constants
BACKGROUND_COLOR = "#B1DDC6"
FRONT_CARD_PATH = "images\card_front.png"
BACK_CARD_PATH = "images\card_back.png"
WRONG_BUTTON_PATH = "images\wrong.png"
RIGHT_BUTTON_PATH = 'images/right.png'

# --------------------------------- CSV Reading Config---------------------------# 
try:
    data = pandas.read_csv("data/Words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
finally:
    data_french_word_list = data["French"].to_list()
    data_english_word_list = data["English"].to_list()

# --------------------------------- Class FlipCard ---------------------------#
class FlipCard:

    def __init__(self,french_list, english_list):
        self.french_list = french_list
        self.english_list = english_list
        self.french_word = ''
        self.english_word = ''
        self.word_index = 0
        self.know_it = {
            "French": [],
            "English": []
        }

    def random_card(self):
        """Generate random word from data french list"""
        canvas.itemconfig(card_bg, image = card_front)

        self.word_index = random.randint(0, len(self.french_list)-1)
        self.french_word = self.french_list[self.word_index]
        self.english_word = self.english_list[self.word_index]

        canvas.itemconfig(title_text, text="French", fill="black")
        canvas.itemconfig(word_text, text=self.french_word, fill="black")

    
        def flip_card():
            """Changing canvas image, Title and Word to English translation"""
            canvas.itemconfig(card_bg, image = card_back)
            canvas.itemconfig(title_text, text="English", fill="white")
            canvas.itemconfig(word_text, text=self.english_word, fill="white")
    
        window.after(3000, flip_card)

    def save_progress(self):
        """Taking element from word lists and appending them to know_it- list"""
        self.know_it["French"].append(self.french_list.pop(self.word_index))
        self.know_it["English"].append(self.english_list.pop(self.word_index))
    
    def multi_func_call(self):
        self.save_progress()
        self.random_card()



# --------------------------------- UI SETUP ---------------------------#

window = Tk()
window.title("Flash card")
window.config(padx=100, pady=50, bg=BACKGROUND_COLOR)

# Card definition

card_front = PhotoImage(file=FRONT_CARD_PATH)
card_back = PhotoImage(file=BACK_CARD_PATH)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_bg = canvas.create_image(400, 263, image=card_front)
title_text = canvas.create_text(400, 160, text="Title", fill="black", font=("Arial", 20, "italic"))
word_text = canvas.create_text(400, 270, text="Word", fill="Black", font=("Arial", 35, "bold"))
canvas.grid(column=1, row=0)

# Starting func.

flipcard = FlipCard(data_french_word_list, data_english_word_list)
flipcard.random_card()

# Buttons

wrong_button_image = PhotoImage(file=WRONG_BUTTON_PATH)
wrong_button = Button(highlightthickness=0, image =wrong_button_image, bd=0, command = flipcard.random_card )
wrong_button.grid(column = 0 , row = 1 )


right_button_image = PhotoImage(file=RIGHT_BUTTON_PATH)
right_button = Button(highlightthickness=0, image =right_button_image, bd=0, command = flipcard.multi_func_call )
right_button.grid(column = 2 , row = 1 )


window.mainloop()



# Create new dic and export it to new file
missing_words = {
    "French": [],
    "English": []
}


for fword in data_french_word_list:
            if fword not in flipcard.know_it:
                missing_words["French"].append(fword)
for eword in data_english_word_list:
            if eword not in flipcard.know_it:
                missing_words["English"].append(eword)
new_data = pandas.DataFrame(missing_words)
new_data.to_csv("data/Words_to_learn.csv", index=False)

