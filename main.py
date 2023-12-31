import customtkinter as ctk
import requests
import crypt
from tkinter import font
from cryptography.fernet import Fernet
import tkinter.messagebox as messagebox
import json

def check_password(plaintext_password, hashed_password):
    return crypt.crypt(plaintext_password, hashed_password) == hashed_password

canvas_list = []

url = 'http://example.com/path/to/remote_file.json'
response = requests.get(url)
root = ctk.CTk()
root.geometry('640x480')
root.minsize(640, 480)
root.maxsize(640, 480)
root.title("Login System Alpha")

def destroy_all_canvases():
    for canvas in canvas_list:
        canvas.destroy()
    canvas_list.clear()

def signup(event):
    destroy_all_canvases()
    signuppagecanvas = ctk.CTkCanvas(root, background="black")
    signuppagecanvas.pack(fill=ctk.BOTH, expand=True)
    back.lift(signuppagecanvas)
    canvas_list.append(signuppagecanvas)
    label = ctk.CTkLabel(signuppagecanvas, text="Sign up to Nexum Alpha",
                         fg_color="transparent", font=('Calibri Light', 17), text_color='white')
    label.place(x=230, y=80)
    uslabel = ctk.CTkLabel(signuppagecanvas, text="Username :",
                           fg_color="transparent", font=('arial', 15), text_color='white')
    uslabel.place(x=210, y=110)
    us_rentry = ctk.CTkEntry(master=signuppagecanvas, width=300, font=("arial", 17), text_color='white', fg_color='gray')
    us_rentry.place(x=180, y=140)
    pwlabel = ctk.CTkLabel(signuppagecanvas, text="Password :",
                           fg_color="transparent", font=('arial', 15), text_color='white')
    pwlabel.place(x=210, y=170)
    pw_entry = ctk.CTkEntry(master=signuppagecanvas, width=300, font=("arial", 17), show="*", text_color='white', fg_color='gray')
    bool_var = ctk.BooleanVar()
    bool_button = ctk.CTkCheckBox(
        root, text="Network Registering", variable=bool_var, bg_color='black', text_color='white')
    bool_button.place(x=380, y=240)
    pw_entry.place(x=180, y=200)

    def on_register_button_click(event):
        password = pw_entry.get()
        username = us_rentry.get()
        register(username, password)

    register_Button = ctk.CTkButton(signuppagecanvas, text="Register")
    register_Button.place(x=220, y=240)
    register_Button.bind("<Button-1>", on_register_button_click)

def getback(event=None):
    destroy_all_canvases()
    maincanvas.pack(fill=ctk.BOTH, expand=True)

    #back.bind("<Button-1>", getback)


def login():
    maincanvas.destroy()
    loginpagecanvas = ctk.CTkCanvas(root, background="black")
    loginpagecanvas.pack(fill=ctk.BOTH, expand=True)
    back.lift(loginpagecanvas)
    canvas_list.append(loginpagecanvas)
    label = ctk.CTkLabel(loginpagecanvas, text="Log Into Nexum Alpha",
                         fg_color="transparent", font=('Calibri Light', 17), text_color='white')
    label.place(x=230, y=80)
    uslabel = ctk.CTkLabel(loginpagecanvas, text="Username :",
                           fg_color="transparent", font=('arial', 15), text_color='white')
    uslabel.place(x=210, y=110)
    usentry = ctk.CTkEntry(master=loginpagecanvas, width=300, font=("arial", 17), text_color='white', fg_color='gray')
    usentry.place(x=180, y=140)
    pwlabel = ctk.CTkLabel(loginpagecanvas, text="Password :",
                           fg_color="transparent", font=('arial', 15), text_color='white')
    pwlabel.place(x=210, y=170)
    pwentry = ctk.CTkEntry(master=loginpagecanvas, width=300, font=("arial", 17), show="*", text_color='white', fg_color='gray')
    bool_var = ctk.BooleanVar()
    bool_button = ctk.CTkCheckBox(
        loginpagecanvas, text="Network Login", variable=bool_var, bg_color='black', text_color='white')
    bool_button.place(x=380, y=240)
    pwentry.place(x=180, y=200)

    # Use lambda to pass the function with arguments without executing it immediately
    loginButton = ctk.CTkButton(loginpagecanvas, text="Log In", command=lambda: log_in_local(username=usentry.get(), password=pwentry.get(), loginpagecanvas=loginpagecanvas))
    loginButton.place(x=220, y=240)

# ... (remaining code

def log_in(bool_var, usentry, pwentry):
    if bool_var.get():
        print("Connecting to server...")
        username = usentry.get()
        password = pwentry.get()
        status = log_in_network(username=username, password=password)
        if status == 'error':
            root.destroy()
    else:
        print("Using offline connection")
        username = usentry.get()
        password = pwentry.get()

# region Server Connection


def log_in_network(username, password):
    if response.status_code == 200:
        content = response.text
    else:
        print(
            f"Failed to connect to our server. Status code: {response.status_code}")
        return 'error'
# endregion

# region Local Way



def log_in_local(username, password):
    with open('data/accounts/accounts.json', 'r') as json_file:
        existing_data = json.load(json_file)

    for user_data in existing_data:
        if username in user_data:
            hashed_password = user_data[username]['password']
            if check_password(password, hashed_password):
                messagebox.showinfo('Signed in as', username)
                return True
            else:
                messagebox.showinfo('Password incorrect :(')
                return False
            break
    else:
        print(f"User '{username}' not found.")
        return False
# endregion



def register(username, password):
    salt = "random_salt"
    hashed_password = crypt.crypt(password, salt)
    data = {
        str(username): {
            'password': str(hashed_password),
            'email': "",
            'phone': ''
        }
    }

    try:
        with open('data/accounts/accounts.json', 'r') as json_file:
            existing_data = json.load(json_file)
            messagebox.showinfo('Registered as', username)
    except FileNotFoundError:
        messagebox.showinfo('An internal error has occured :(')
    existing_data.dump()
    with open('data/accounts/accounts.json', 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)



#back.bind("<Button-1>", getback)
maincanvas = ctk.CTkCanvas(root, background="black")
maincanvas.pack(fill=ctk.BOTH, expand=True)
canvas_list.append(maincanvas)
back = ctk.CTkButton(root, text="back", command=getback)
back.place(x=20, y=20)
back.lift(maincanvas)
log_inButton = ctk.CTkButton(maincanvas, text="Log In", command=login)
log_inButton.place(x=330, y=200)
sign_upButton = ctk.CTkButton(maincanvas, text="Sign Up")
sign_upButton.bind("<Button-1>", signup)
sign_upButton.place(x=170, y=200)


root.mainloop()