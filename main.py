import tkinter as tk
from tkinter import messagebox
import password_manager as pm

try:
    open("secret.key", "rb")
except FileNotFoundError:
    pm.generate_key()
pm.init_db()

root = tk.Tk()
root.title("🔐 Password Manager")
root.geometry("400x350")
root.resizable(False, False)

tk.Label(root, text="Website:").pack(pady=5)
website_entry = tk.Entry(root, width=40)
website_entry.pack()

tk.Label(root, text="Username:").pack(pady=5)
username_entry = tk.Entry(root, width=40)
username_entry.pack()

tk.Label(root, text="Password:").pack(pady=5)
password_entry = tk.Entry(root, width=40, show="*")
password_entry.pack()

def generate_password():
    new_pass = pm.generate_password()
    password_entry.delete(0, tk.END)
    password_entry.insert(0, new_pass)

def save_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if not website or not username or not password:
        messagebox.showerror("Error", "All fields required!")
        return

    pm.save_password(website, username, password)
    messagebox.showinfo("Success", "Password saved securely!")
    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

def retrieve_password():
    website = website_entry.get()
    if not website:
        messagebox.showerror("Error", "Enter a website name!")
        return

    username, password = pm.get_password(website)
    if username:
        messagebox.showinfo("Retrieved", f"Username: {username}\nPassword: {password}")
    else:
        messagebox.showwarning("Not Found", "No credentials found for this website.")

tk.Button(root, text="Generate Password", command=generate_password).pack(pady=8)
tk.Button(root, text="Save Password", command=save_password).pack(pady=8)
tk.Button(root, text="Retrieve Password", command=retrieve_password).pack(pady=8)

root.mainloop()
