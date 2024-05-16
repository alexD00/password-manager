from tkinter import *
from tkinter import messagebox
from characters import *
import random
import pyperclip
import json


def save_to_file():
    new_data = {
        website_entry.get(): {
            "email": email_entry.get(),
            "password": password_entry.get()
        }
    }
    if len(website_entry.get()) == 0 or len(email_entry.get()) == 0 or len(password_entry.get()) == 0:
        messagebox.showerror(title="Error", message="Please fill out all fields")
        return

    # Using a txt file
    # with open("passwords.txt", "a") as file:  # Use append mode ('a') instead of write mode ('w')
    #     file.write(f"{website_entry.get()} | {email_entry.get()} | {password_entry.get()} \n")

    # Using a json file
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        with open("data.json", "w") as file:
            json.dump(new_data, file, indent=4)
    else:
        with open("data.json", "w") as file:
            data.update(new_data)
            json.dump(data, file, indent=4)

    messagebox.showinfo(title="Password saved!", message=f"Data for '{website_entry.get()}' was saved successfully!")

    website_entry.delete(0, "end")
    email_entry.delete(0, "end")
    password_entry.delete(0, "end")


def generate_password():
    password_entry.delete(0, "end")
    generated_password = ""
    password_list = []
    num_of_letters = [3, 4, 5]

    for _ in range(random.choice(num_of_letters)):
        password_list.append(random.choice(lower_case_letters))
    for _ in range(random.choice(num_of_letters)):
        password_list.append(random.choice(upper_case_letters))
    for _ in range(random.choice(num_of_letters)):
        password_list.append(random.choice(numbers))
    for _ in range(random.choice(num_of_letters)):
        password_list.append(random.choice(symbols))

    random.shuffle(password_list)
    for i in password_list:
        generated_password += i

    password_entry.insert(0, generated_password)
    pyperclip.copy(generated_password)


def search_website():
    website_name = website_entry.get()

    if len(website_name) == 0:
        messagebox.showerror(title="Error", message=f"Please type a website")
    else:
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            messagebox.showerror(title="Error", message=f"Error no data file found")
        else:
            try:
                messagebox.showinfo(title=f"Success", message=f"Info for {website_name}:"
                                                              f"\nemail: {data[website_name]['email']}"
                                                              f"\npassword: {data[website_name]['password']}")
            except KeyError:
                messagebox.showerror(title="Error", message=f"You do not have data saved for website: {website_name}")


window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40, bg="#67C6E3")

canvas = Canvas(width=400, height=200, bg="#67C6E3", highlightthickness="0")
password_image = PhotoImage(file="password_logo.png")
canvas.create_image(200, 100, image=password_image)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:", bg="#67C6E3", font=("Arial", 32))
website_label.grid(column=0, row=1)

website_entry = Entry(width=22, highlightthickness="0", font=("Arial", 25))
website_entry.grid(column=1, row=1)

email_label = Label(text="Email/Username:", bg="#67C6E3", font=("Arial", 32))
email_label.grid(column=0, row=2)

email_entry = Entry(width=22, highlightthickness="0", font=("Arial", 25))
email_entry.grid(column=1, row=2)

password_label = Label(text="Password:", bg="#67C6E3", font=("Arial", 32))
password_label.grid(column=0, row=3)

password_entry = Entry(width=22, highlightthickness="0", font=("Arial", 25))
password_entry.grid(column=1, row=3)

search_btn = Button(text="Search", width=15, command=search_website, font=("Arial", 20),
                    highlightbackground="gray", highlightthickness=2)
search_btn.grid(column=2, row=1, pady=(10, 0))

generate_pass_btn = Button(text="Generate Password", command=generate_password, font=("Arial", 20),
                           highlightbackground="gray", highlightthickness=2)
generate_pass_btn.grid(column=2, row=3)

add_btn = Button(text="Add", width=24, command=save_to_file, font=("Arial", 20),
                 highlightbackground="gray", highlightthickness=2)
add_btn.grid(column=1, row=4, pady=(10, 0))

window.mainloop()
