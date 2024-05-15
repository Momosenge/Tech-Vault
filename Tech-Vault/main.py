import tkinter as tk
from tkinter import messagebox
import random
import string

def main():
    root = tk.Tk()
    root.title("Tech Vault")

    welcome_label = tk.Label(root, text="Welcome to Tech Vault", font=("Arial", 14))
    welcome_label.pack(pady=10)

    choice_label = tk.Label(root, text="Enter 'login' to login or 'register' to create a new account:")
    choice_label.pack()

    choice_entry = tk.Entry(root)
    choice_entry.pack(pady=5)

    login_register_button = tk.Button(root, text="Login/Register", command=lambda: on_login_register(root, choice_entry.get()))
    login_register_button.pack(pady=5)

    root.mainloop()

def on_login_register(root, choice):
    if choice.lower() == 'login':
        login(root)
    elif choice.lower() == 'register':
        register(root)
    else:
        messagebox.showerror("Error", "Invalid choice. Please enter 'login' or 'register'.")

def login(root):
    login_window = tk.Toplevel(root)
    login_window.title("Login")

    username_label = tk.Label(login_window, text="Username:")
    username_label.pack()

    username_entry = tk.Entry(login_window)
    username_entry.pack()

    password_label = tk.Label(login_window, text="Password:")
    password_label.pack()

    global password_entry
    password_entry = tk.Entry(login_window, show="*")  # Hide password by default
    password_entry.pack()

    show_password = False  # Flag to track password visibility

    def toggle_password_visibility():
        nonlocal show_password
        show_password = not show_password
        password_entry.config(show="" if show_password else "*")

    show_password_checkbox = tk.Checkbutton(login_window, text="Show Password", command=toggle_password_visibility)
    show_password_checkbox.pack()

    login_button = tk.Button(login_window, text="Login", command=lambda: on_login(login_window, username_entry.get(), password_entry.get()))
    login_button.pack()

def on_login(login_window, username, password):
    users = read_user_data('bankdata.txt')
    if login_user(users, username, password):
        messagebox.showinfo("Login", "Login Successful!")
        login_window.destroy()
        process_transaction(username, users)
    else:
        messagebox.showerror("Error", "Invalid username or password")

def register(root):
    register_window = tk.Toplevel(root)
    register_window.title("Register")

    username_label = tk.Label(register_window, text="Desired Username:")
    username_label.pack()

    username_entry = tk.Entry(register_window)
    username_entry.pack()

    register_button = tk.Button(register_window, text="Register", command=lambda: on_register(register_window, username_entry.get()))
    register_button.pack()

def on_register(register_window, username):
    account_number = generate_account_number()
    password = generate_password()

    # Create a new file for the user
    filename = f"{username}.txt"
    with open(filename, 'w') as f:
        f.write(f"Username: {username}\n")
        f.write(f"Account Number: {account_number}\n")
        f.write(f"Password: {password}\n")

    # Append the user's information to the main database file
    with open('bankdata.txt', 'a') as f:
        f.write(f"{username},{account_number},{password}\n")

    messagebox.showinfo("Registration", f"Account successfully created!\nUsername: {username}\nAccount Number: {account_number}\nPassword: {password}")
    register_window.destroy()


    with open('bankdata.txt', 'a') as f:
        f.write(f"{username},{account_number},{password}\n")

    messagebox.showinfo("Registration", f"Account successfully created!\nUsername: {username}\nAccount Number: {account_number}\nPassword: {password}")
    register_window.destroy()

def read_user_data(filename):
    users = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    username, account, pwd = parts
                    balance = 1000  # Assuming default balance is 1000
                    users[username] = (account, pwd, balance)
    except FileNotFoundError:
        print("Error: File not found.")
    except Exception as e:
        print(f"Error: {e}")
    return users

def login_user(users, username, password):
    if username in users:
        stored_password = users[username][1]
        if stored_password == password:
            return True
    return False

def generate_account_number():
    return ''.join(random.choices(string.digits, k=8))

def generate_password():
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits
    special_characters = '!@#$%^&*()'

    password_characters = uppercase_letters + lowercase_letters + digits + special_characters
    return ''.join(random.choices(password_characters, k=12))

def process_transaction(username, users):
    transaction_window = tk.Toplevel()
    transaction_window.title("Transactions")

    transaction_label = tk.Label(transaction_window, text="Select transaction type:")
    transaction_label.pack()

    transaction_var = tk.StringVar(transaction_window, "1")  # Default value for transaction type
    transaction_radios = [
        ("Withdraw", "1"),
        ("Deposit", "2")
    ]

    for text, value in transaction_radios:
        radio = tk.Radiobutton(transaction_window, text=text, variable=transaction_var, value=value)
        radio.pack()

    amount_label = tk.Label(transaction_window, text="Enter amount (in Rands):")
    amount_label.pack()

    amount_entry = tk.Entry(transaction_window)
    amount_entry.pack()

    confirm_button = tk.Button(transaction_window, text="Confirm", command=lambda: confirm_transaction(username, users, transaction_window, transaction_var.get(), amount_entry.get()))
    confirm_button.pack()

def confirm_transaction(username, users, transaction_window, transaction_type, amount):
    if transaction_type == '1':
        # Withdrawal transaction
        if amount.isdigit():
            amount = int(amount)
            if users[username][2] >= amount:
                # Update user's balance
                users[username] = (users[username][0], users[username][1], users[username][2] - amount)
                messagebox.showinfo("Withdrawal", f"Withdrawal of {amount} Rands successful.\nCurrent balance: {users[username][2]} Rands")
            else:
                messagebox.showerror("Error", "Insufficient balance.")
        else:
            messagebox.showerror("Error", "Invalid amount.")
    elif transaction_type == '2':
        # Deposit transaction
        if amount.isdigit():
            amount = int(amount)
            # Update user's balance
            users[username] = (users[username][0], users[username][1], users[username][2] + amount)
            messagebox.showinfo("Deposit", f"Deposit of {amount} Rands successful.\nCurrent balance: {users[username][2]} Rands")
        else:
            messagebox.showerror("Error", "Invalid amount.")
    else:
        messagebox.showerror("Error", "Invalid transaction type.")

    # Append transaction details to TransactionLog.txt
    with open('TransactionLog.txt', 'a') as f:
        f.write(f"{username}, {transaction_type}, {amount}\n")

    # Write the updated user data to the bankdata.txt file
    with open('bankdata.txt', 'w') as f:
        for user, data in users.items():
            f.write(f"{user},{data[0]},{data[1]},{data[2]}\n")

    transaction_window.destroy()

if __name__ == "__main__":
    main()

