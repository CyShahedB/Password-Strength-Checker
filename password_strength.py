import tkinter as tk
from tkinter import messagebox
import re
import os

# Allowed symbols regex
allowed_symbols = r"[!@#$%^&*(),.?\":{}|<>]"

# Check function
def check_password_strength():
    password = password_var.get().strip()

    # Check if empty
    if not password:
        messagebox.showwarning("Empty", "⚠️ Please enter a password!")
        return

    # Check for invalid symbols
    invalid_symbols = []
    for char in password:
        if not re.match(allowed_symbols, char) and not char.isalnum():
            invalid_symbols.append(char)

    if invalid_symbols:
        messagebox.showerror("Invalid Symbol", f"❌ Invalid symbol(s): {', '.join(invalid_symbols)}\nOnly !@#$%^&*(),.?\":{{}}|<> are allowed.")
        return

    # Check against common passwords
    if os.path.exists("common_passwords.txt"):
        with open("common_passwords.txt", "r") as file:
            common_passwords = file.read().splitlines()
        if password in common_passwords:
            messagebox.showerror("Too Common", "❌ This password is too common! Please choose a stronger one.")
            return

    errors = []

    if len(password) < 8:
        errors.append("🔸 Minimum 8 characters")
    if re.search(r"[a-z]", password) is None:
        errors.append("🔸 Lowercase letter (a–z)")
    if re.search(r"[A-Z]", password) is None:
        errors.append("🔸 Uppercase letter (A–Z)")
    if re.search(r"\d", password) is None:
        errors.append("🔸 Digit (0–9)")
    if re.search(allowed_symbols, password) is None:
        errors.append("🔸 Symbol (!@#$...)")

    score = 5 - len(errors)

    if score == 5:
        messagebox.showinfo("Strong Password", "✅ Strong password!")
    elif 3 <= score < 5:
        messagebox.showwarning("Moderate Password", "🟡 Moderate password!\n\nMissing:\n" + "\n".join(errors))
    else:
        messagebox.showerror("Weak Password", "❌ Weak password.\n\nMissing:\n" + "\n".join(errors))


# Toggle show/hide password
def toggle_password():
    if password_entry.cget('show') == '':
        password_entry.config(show='*')
        toggle_btn.config(text='👁')
    else:
        password_entry.config(show='')
        toggle_btn.config(text='❌')


# GUI setup
root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("400x250")
root.resizable(False, False)

tk.Label(root, text="Enter your password:", font=("Arial", 12)).pack(pady=10)

password_var = tk.StringVar()
password_entry = tk.Entry(root, textvariable=password_var, show='*', width=30, font=("Arial", 12))
password_entry.pack()

toggle_btn = tk.Button(root, text='👁', command=toggle_password, font=("Arial", 10))
toggle_btn.pack(pady=5)

check_btn = tk.Button(root, text="Check Password", command=check_password_strength, bg="#4CAF50", fg="white", font=("Arial", 12))
check_btn.pack(pady=15)

root.mainloop()
