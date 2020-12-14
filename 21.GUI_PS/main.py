from tkinter import *
from tkinter import messagebox
import pyperclip
import random
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def random_password():
    
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    Password_array = []
    Password = ""

    Password_input.delete(0, END)

    for i in range(0, 8):
        Password_array.append(random.choice(letters))
    for j in range(0, 2):
        Password_array.append(random.choice(symbols))
    for k in range(0, 2):
        Password_array.append(random.choice(numbers))

    for char in range(0, len(Password_array)):
        choice = random.randint(0, len(Password_array))
        Password += Password_array.pop(choice - 1)
    
    
    Password_input.insert(0, Password)
    pyperclip.copy(Password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    
    website = website_input.get()
    email_username = Email_Username_input.get()
    password = Password_input.get()

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Error", message="Please don't leave any fields empty!")
    else:
        decision = messagebox.askokcancel(title=website, message=f"These are details entered: \n Email: {email_username}\n Password: {password}\n Is it okay to save?")

        if decision:
            password_line = f"{website} | {email_username} | {password}"
            
            with open("password.txt", mode="a+") as password_file:
                # Move read cursor to the start of file. 
                password_file.seek(0)
                # If file is not empty then append '\n'
                data = password_file.read(100)
                if len(data) > 0 :
                    password_file.write("\n")
                # Append text at the end of file
                password_file.write(password_line)

                website_input.delete(0, END)
                Password_input.delete(0, END)
                messagebox.showinfo(title="Password Manager", message="Details succesfully saved into password.txt")
        else:
            website_input.delete(0, END)
            Password_input.delete(0, END)
        

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=100, pady=50)




canvas = Canvas(width=200, height=189)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 95, image=lock_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.grid(column = 0, row = 1)
Email_Username_label = Label(text="Email/Username:")
Email_Username_label.grid(column = 0, row = 2)
Password_label = Label(text="Password:")
Password_label.grid(column = 0, row = 3)

#  Entry
website_input = Entry(width = 55)
website_input.grid(column = 1 , row = 1, columnspan = 2)
Email_Username_input = Entry(width = 55)
Email_Username_input.grid(column =1, row = 2, columnspan = 2)
Email_Username_input.insert(0, "mlynskimax@gmail.com")
Password_input = Entry(width = 36)
Password_input.grid(column = 1 , row = 3)

# Buttons
Password_button = Button(text="Generate Password", command = random_password)
Password_button.grid(column = 2 , row = 3)
add_button = Button(text="Add", width = 47, command = save)
add_button.grid(column = 1 , row = 4, columnspan = 2)


window.mainloop()

