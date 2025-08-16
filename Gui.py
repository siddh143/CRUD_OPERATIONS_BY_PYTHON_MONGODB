from pymongo import MongoClient
import tkinter as tk
from tkinter import messagebox, ttk


client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["users"]


def insert_user(name, age):
    collection.insert_one({"name": name, "age": age})

def get_all_users():
    return list(collection.find())

def update_user(name, new_age):
    collection.update_one({"name": name}, {"$set": {"age": new_age}})

def delete_user(name):
    collection.delete_one({"name": name})


root = tk.Tk()
root.title("MongoDB CRUD with Tkinter")
root.geometry("500x400")


name_label = tk.Label(root, text=" SIDDHARTH_YADAV (Roll No: 553)",
                      font=("Arial", 12, "bold"), fg="blue")
name_label.grid(row=0, column=0, columnspan=3, pady=10)


tk.Label(root, text="Name").grid(row=1, column=0, padx=5, pady=5)
entry_name = tk.Entry(root)
entry_name.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Age").grid(row=2, column=0, padx=5, pady=5)
entry_age = tk.Entry(root)
entry_age.grid(row=2, column=1, padx=5, pady=5)


tk.Button(root, text="Add", command=lambda: add_user()).grid(row=3, column=0, pady=5)
tk.Button(root, text="Update", command=lambda: update_selected()).grid(row=3, column=1, pady=5)
tk.Button(root, text="Delete", command=lambda: delete_selected()).grid(row=3, column=2, pady=5)
tk.Button(root, text="Refresh", command=lambda: refresh_table()).grid(row=4, column=1, pady=5)


tree = ttk.Treeview(root, columns=("Name", "Age"), show="headings")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.grid(row=5, column=0, columnspan=3, padx=5, pady=5)


def refresh_table():
    for i in tree.get_children():
        tree.delete(i)
    for user in get_all_users():
        tree.insert("", "end", values=(user["name"], user["age"]))

def add_user():
    name = entry_name.get()
    age = entry_age.get()
    if name and age:
        try:
            insert_user(name, int(age))
            refresh_table()
            messagebox.showinfo("Success", "User added!")
        except ValueError:
            messagebox.showerror("Error", "Age must be a number")
    else:
        messagebox.showerror("Error", "Please enter name and age")

def update_selected():
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "Select a row to update")
        return
    values = tree.item(selected, "values")
    new_age = entry_age.get()
    if new_age:
        try:
            update_user(values[0], int(new_age))
            refresh_table()
            messagebox.showinfo("Updated", "User updated!")
        except ValueError:
            messagebox.showerror("Error", "Age must be a number")
    else:
        messagebox.showerror("Error", "Please enter new age")

def delete_selected():
    selected = tree.focus()
    if not selected:
        messagebox.showerror("Error", "Select a row to delete")
        return
    values = tree.item(selected, "values")
    delete_user(values[0])
    refresh_table()
    messagebox.showinfo("Deleted", "User deleted!")


refresh_table()

root.mainloop()
