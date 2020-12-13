import pandas
from tkinter import *

data = pandas.read_csv("nato_phonetic_alphabet.csv")
phonetic_dict = {row.letter: row.code for (index, row) in data.iterrows()}



def alphabet_to_NATO():
    word_normal = word_input.get().upper()
    output_list = [phonetic_dict[letter] for letter in word_normal]
    Nato_text = ', '.join(output_list)
    nato_result.config(text=Nato_text)

window = Tk()
window.title("Nato alphabet converter")
window.config(padx = 20, pady = 20)
window.minsize(width=300, height=100)

word_input = Entry(width=30)
word_input.grid(column=1, row=0)


label_insert_word = Label(text="Insert word")
label_insert_word.grid(column=0, row=0)

nato_alphabet = Label(text="In nato alphabet =>")
nato_alphabet.grid(column=0, row=1)

nato_result = Label(text="NATO")
nato_result.grid(column=1, row=1)

convert_button = Button(text="Convert", command = alphabet_to_NATO)
convert_button.grid(column=2, row=0)





window.mainloop()